from pydantic import BaseModel, Field

class AnalyticsCategoryOut(BaseModel):
	code: str = Field(min_length=1)
	name: str = Field(min_length=1)
	requests_count: int = Field(ge=0)


class AnalyticsOut(BaseModel):
	total_requests: int = Field(ge=0)
	requests_by_cat: list[AnalyticsCategoryOut]
	toxic_rate: float = Field(ge=0.0, le=1.0)
	clarification_requests: int = Field(ge=0)