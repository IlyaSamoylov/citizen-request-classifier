from typing import Any

def _build_schema(allowed_codes: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "categories": {
                "type": "array",
                "items": {"type": "string", "enum": allowed_codes},
                "description": "Список кодов категорий обращения",
            },
            "confidence": {
                "type": "object",
                "additionalProperties": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "description": "Уверенность по каждой категории",
            },
            "is_toxic": {
                "type": "boolean",
                "description": "Является ли обращение токсичным"
            },
            "needs_clarification": {
                "type": "boolean",
                "description": "Нужно ли уточнение перед классификацией",
            },
            "question": {
                "type": ["string", "null"],
                "description": "Вопрос для уточнения, если он нужен",
            },
        },
        "required": ["categories", "confidence", "is_toxic", "needs_clarification", "question"],
        "additionalProperties": False,
    }

def _build_system_prompt(allowed_codes: list[str]) -> str:
    codes = ",".join(allowed_codes)
    return (
        "Ты классификатор обращений. "
        "Верни только JSON по схеме. "
        "Выбирай категории только из списка допустимых кодов ниже. "
        "Не придумывай новые коды. "
        "Если подходит несколько категорий — верни несколько. "
        "Если ни одна категория не подходит верни categories=[]. "
        "Если не хватает информации — верни needs_clarification=true с коротким вопросом на русском языке. "   
        "Определи is_toxic=true, если в обращении есть нецензурная лексика, оскорбления, агрессия "
        "или явная токсичность. is_toxic=false, если этого нет. "
        f"Доступные коды категорий: {codes}. "
        "Не используй markdown, пояснения или лишние поля."
    )
