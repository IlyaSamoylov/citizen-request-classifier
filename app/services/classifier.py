from dataclasses import dataclass


@dataclass
class PredictionResult:
    categories: list[str]
    confidence: dict[str, float]
    needs_clarification: bool = False
    question: str | None = None


class BaseClassifier:
    async def predict(self, text: str) -> PredictionResult:
        raise NotImplementedError


class DummyClassifier(BaseClassifier):
    async def predict(self, text: str) -> PredictionResult:
        text_l = text.lower()

        categories: list[str] = []
        confidence: dict[str, float] = {}

        if any(word in text_l for word in ["дорог", "яма", "асфальт", "разметк", "трасс"]):
            categories.append("roads")
            confidence["roads"] = 0.93

        if any(word in text_l for word in ["дом", "подъезд", "жкх", "квартир", "отоплен", "вода"]):
            categories.append("housing")
            confidence["housing"] = 0.88

        if not categories:
            return PredictionResult(
                categories=[],
                confidence={},
                needs_clarification=True,
                question="Уточните, пожалуйста, к какой сфере относится обращение?",
            )

        return PredictionResult(
            categories=categories,
            confidence=confidence,
        )