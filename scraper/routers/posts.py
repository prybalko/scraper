from operator import itemgetter

from fastapi import APIRouter, Query

from scraper.models.post import Post, get_all_posts

router = APIRouter()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/")
async def get_posts(
        offset: int = Query(0, ge=0),
        limit: int = Query(30, ge=0, le=1000),
        order: str = Query(None),
):
    posts = (await get_all_posts())[offset:offset+limit]
    if order in Post.__fields__:
        posts.sort(key=itemgetter(order))
    return posts
