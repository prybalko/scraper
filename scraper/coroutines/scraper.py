import logging
from asyncio import sleep
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from scraper.models.post import Post, update_posts_cache

HACKERNEWS_URL = 'https://news.ycombinator.com/'

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


async def run_scraper():
    while True:
        await check_new_posts()
        await sleep(30)


async def read_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(HACKERNEWS_URL) as resp:
            return await resp.read()


def parse_hackernews_stories(html):
    soup = BeautifulSoup(html.decode('utf-8'), 'html5lib')
    table = soup.find('table', attrs={'class': 'itemlist'})
    for story in table.find_all('a', attrs={'class': 'storylink'}):
        yield story


async def check_new_posts():
    html = await read_url(HACKERNEWS_URL)
    stories = parse_hackernews_stories(html)
    await Post.delete()
    for i, story in enumerate(stories):
        post = Post(id=i+1, title=story.text, url=urljoin(HACKERNEWS_URL, story['href']))
        await post.save()
    await update_posts_cache()
    logger.info('Posts list updated')
