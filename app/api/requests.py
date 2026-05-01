from fastapi import APIRouter

from app.schemas.requests import RequestIn, RequestOut, RequestFull

requests_router = APIRouter(prefix="/requests", tags=["requests"])

@requests_router.post("", response_model=RequestOut)
async def post_request(request: RequestIn):
	pass

@requests_router.get("/{id}", response_model=RequestFull)
async def get_request(id: int):
	pass

@requests_router.post("/{id}/clarifications")
async def post_clarifications(id: int):
	pass

