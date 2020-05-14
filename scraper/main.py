import asyncio
from asyncio import sleep

from fastapi import FastAPI
from fastapi_contrib.db.utils import setup_mongodb

from scraper.coroutines.scraper import run_scraper
from scraper.routers import index
from scraper.routers import posts

app = FastAPI()


app.include_router(index.router)
app.include_router(posts.router, prefix="/posts")

# mongodb = None

@app.on_event('startup')
async def startup():
    setup_mongodb(app)

    # app.mongodb.create_collection('posts', capped=True, size=10**6, max=30)

    event_loop = asyncio.get_event_loop()
    asyncio.ensure_future(run_scraper(), loop=event_loop)

