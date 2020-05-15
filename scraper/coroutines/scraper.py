import logging
from asyncio import sleep
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientConnectorError
from bs4 import BeautifulSoup

from scraper.models.post import Post

HACKERNEWS_URL = "https://news.ycombinator.com/"
SLEEP_SECONDS = 60

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


async def run_scraper():
    while True:
        await check_new_posts()
        await sleep(SLEEP_SECONDS)


async def read_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


def parse_hackernews_stories(html):
    soup = BeautifulSoup(html.decode("utf-8"), "html5lib")
    table = soup.find("table", attrs={"class": "itemlist"})
    for story in table.find_all("a", attrs={"class": "storylink"}):
        yield story


async def check_new_posts():
    try:
        html = await read_url(HACKERNEWS_URL)
    except ClientConnectorError:
        # Network issues. Try next time.
        return
    stories = parse_hackernews_stories(html)
    # ToDo: make it in a transaction
    await Post.delete()
    for i, story in enumerate(stories):
        post = Post(
            id=i + 1, title=story.text, url=urljoin(HACKERNEWS_URL, story["href"])
        )
        # ToDo: use batch insert
        await post.save()
    await Post.update_cache()
    logger.info("Posts list updated")
