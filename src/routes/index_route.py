from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    name='Health check',
    description="Health check.",
    tags=["health"]
)
async def health():
    return {"status": "ok"}
