from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    return "Welcome to Scraper!"
