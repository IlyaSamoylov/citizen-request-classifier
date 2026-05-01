from pydantic import BaseModel, Field

class AnalyticsOut(BaseModel):
	requests_by_category: dict[str, int]
	toxic_requests_ratio: float
	k_clarifications: int
	accuracy: float | None = Field(default=None, ge=0.0, le=1.0)
	F1: float | None = Field(default=None, ge=0.0, le=1.0)