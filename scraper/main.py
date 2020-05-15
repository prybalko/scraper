import asyncio

from fastapi import FastAPI
from fastapi_contrib.db.utils import setup_mongodb

from scraper.coroutines.scraper import run_scraper
from scraper.routers import index
from scraper.routers import posts

app = FastAPI()

app.include_router(index.router)
app.include_router(posts.router, prefix="/posts")


@app.on_event("startup")
async def startup():
    setup_mongodb(app)

    event_loop = asyncio.get_event_loop()
    asyncio.ensure_future(run_scraper(), loop=event_loop)
