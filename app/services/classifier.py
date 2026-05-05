import httpx
import json
from typing import Any

from app.core.errors import ExternalServiceError, EmptyModelResponseError
from app.services.dataclasses import ChatMessageDomain, PredictionResult
from app.core.config import settings
from app.services.utils import _build_system_prompt, _build_schema

class OpenRouterClassifier:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self._model = settings.OPENROUTER_MODEL
        self._referer = str(settings.OPENROUTER_SITE_URL)
        self._title = settings.OPENROUTER_APP_NAME
        self._base_url = str(settings.OPENROUTER_BASE_URL)
        self._url = f"{self._base_url}/chat/completions"
        self._access_token = settings.OPENROUTER_API_KEY

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "HTTP-Referer": self._referer,
            "X-OpenRouter-Title": self._title
        }

    def _build_payload(self, messages: list[ChatMessageDomain], allowed_codes: list[str], use_so: bool = True) -> dict[str, Any]:
        api_messages: list[dict[str, str]] = [
            {"role": "system", "content": _build_system_prompt(allowed_codes)},
            *[message.to_api() for message in messages]
        ]

        payload: dict[str, Any] = {
            "model": self._model,
            "messages": api_messages,
            "temperature": 0.0,
            "max_completion_tokens": 300,
            "plugins": [{"id": "response-healing"}]
        }

        if use_so:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "ticket_classification",
                    "strict": True,
                    "schema": _build_schema(allowed_codes)
                }
            }

        return payload

    @staticmethod
    def _load_prediction_json(content: str) -> dict[str, Any]:
        try:
            raw = json.loads(content)
        except json.JSONDecodeError as e:
            raise ExternalServiceError("OpenRouter вернул невалидный JSON") from e

        if not isinstance(raw, dict):
            raise ExternalServiceError("OpenRouter вернул JSON не того формата")

        return raw

    @staticmethod
    def _parse_categories(raw_value, allowed_codes: set[str]) -> list[str]:
        if not isinstance(raw_value, list):
            raise ExternalServiceError("Поле categories должно быть списком")

        categories: list[str] = []
        for item in raw_value:
            if not isinstance(item, str) or not item.strip():
                raise ExternalServiceError("categories содержит некорректный код категории")
            normalized = item.strip()
            if normalized not in allowed_codes:
                raise ExternalServiceError(f"Модель вернула недопустимый код категории: {normalized}")
            if normalized not in categories:
                categories.append(normalized)
        return categories

    @staticmethod
    def _parse_confidence(raw_value, allowed_codes: set[str]) -> dict[str, float]:
        if not isinstance(raw_value, dict):
            raise ExternalServiceError("Поле confidence должно быть объектом")

        confidence: dict[str, float] = {}
        for code, value in raw_value.items():
            if not isinstance(code, str) or not code.strip():
                raise ExternalServiceError("confidence содержит некорректный ключ")
            if code not in allowed_codes:
                raise ExternalServiceError(f"confidence содержит недопустимый код: {code}")
            if not isinstance(value, (int, float)):
                raise ExternalServiceError(f"confidence[{code}] должно быть числом")
            float_value = float(value)
            if not 0.0 <= float_value <= 1.0:
                raise ExternalServiceError(f"confidence[{code}] должно быть в диапазоне 0..1")
            confidence[code] = float_value

        return confidence

    @staticmethod
    def _parse_clarification(raw_needs, raw_question) -> tuple[bool, str | None]:
        if not isinstance(raw_needs, bool):
            raise ExternalServiceError("Поле needs_clarification должно быть bool")

        if raw_question is not None and not isinstance(raw_question, str):
            raise ExternalServiceError("Поле question должно быть строкой или null")

        question = raw_question.strip() if isinstance(raw_question, str) else None
        if question == "":
            question = None

        if raw_needs and question is None:
            raise ExternalServiceError("Если needs_clarification=true, поле question должно быть непустым")

        if not raw_needs:
            question = None

        return raw_needs, question

    @staticmethod
    def _parse_prediction(content: str, allowed_codes: set[str]) -> PredictionResult:
        raw = OpenRouterClassifier._load_prediction_json(content)

        try:
            is_toxic_raw = raw["is_toxic"]
            categories_raw = raw["categories"]
            confidence_raw = raw["confidence"]
            needs_raw = raw["needs_clarification"]
            question_raw = raw["question"]
        except KeyError as e:
            raise ExternalServiceError(f"Ответ OpenRouter не содержит обязательного поля  {e.args[0]}") from e

        if not isinstance(is_toxic_raw, bool):
            raise ExternalServiceError("Поле is_toxic должно быть bool")

        categories = OpenRouterClassifier._parse_categories(categories_raw, allowed_codes)
        confidence = OpenRouterClassifier._parse_confidence(confidence_raw, allowed_codes)
        needs_clarification, question = OpenRouterClassifier._parse_clarification(needs_raw, question_raw)

        return PredictionResult(
            categories=categories,
            confidence=confidence,
            is_toxic=is_toxic_raw,
            needs_clarification=needs_clarification,
            question=question,
        )

    def _extract_content(self, resp: httpx.Response) -> str:
        try:
            raw = resp.json()
        except ValueError as exc:
            raise ExternalServiceError("OpenRouter вернул не JSON") from exc

        if isinstance(raw, dict) and "error" in raw:
            raise ExternalServiceError(f"OpenRouter error payload: {raw['error']}")

        try:
            content = raw["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ExternalServiceError("Неверный формат ответа от OpenRouter") from exc

        if not isinstance(content, str) or not content.strip():
            raise EmptyModelResponseError("OpenRouter вернул пустой content")
        return content

    async def _predict_once(self, payload: dict[str, Any], allowed_codes_set: set[str]) -> PredictionResult:
        response = await self._client.post(self._url, json=payload, headers=self._headers())
        response.raise_for_status()

        content = self._extract_content(response)
        return self._parse_prediction(content, allowed_codes_set)

    async def predict(self, messages: list[ChatMessageDomain], allowed_codes: list[str]) -> PredictionResult:

        if not allowed_codes:
            raise ExternalServiceError("Категории не переданы модели")
        allowed_codes_set = set(allowed_codes)

        for retry in range(settings.LLM_MAX_RETRIES + 1):
            try:
                structured_payload = self._build_payload(messages=messages, allowed_codes=allowed_codes, use_so=True)
                return await self._predict_once(structured_payload, allowed_codes_set)

            except EmptyModelResponseError:
                if retry < settings.LLM_MAX_RETRIES:
                    continue
                raise ExternalServiceError("OpenRouter вернул пустой ответ несколько раз")

            except httpx.HTTPStatusError as e:
                body = e.response.text.lower()
                if e.response.status_code in {400, 422} and "response_format" in body:
                    payload = self._build_payload(messages=messages, allowed_codes=allowed_codes, use_so=False)
                    return await self._predict_once(payload, allowed_codes_set)

                if 500 <= e.response.status_code < 600 and retry < settings.LLM_MAX_RETRIES:
                    continue

                raise ExternalServiceError(f"Ошибка OpenRouter: {e.response.status_code} {e.response.text}") from e

            except ExternalServiceError as e:
                if "response_format" not in str(e).lower() and "structured output" not in str(e).lower():
                    raise

        payload = self._build_payload(messages=messages, allowed_codes=allowed_codes, use_so=False)
        return await self._predict_once(payload, allowed_codes_set)
