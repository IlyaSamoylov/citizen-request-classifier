class BaseToxicityDetector:
    async def detect(self, text: str) -> bool:
        raise NotImplementedError


class DummyToxicityDetector(BaseToxicityDetector):
    BAD_WORDS = [
        "сука",
        "бляд",
        "еба",
        "хуй",
        "пизд",
        "мудак",
        "урод",
        "сволоч",
        "угрожа",
    ]

    async def detect(self, text: str) -> bool:
        text_l = text.lower()
        return any(token in text_l for token in self.BAD_WORDS)