from datetime import datetime
from typing import List, Optional

from fastapi_contrib.db.models import MongoDBModel, MongoDBTimeStampedModel


class Post(MongoDBTimeStampedModel):
    id: int
    title: str
    url: str

    class Meta:
        collection = "posts"


_CACHED_POSTS: Optional[List[Post]] = None


async def get_all_posts() -> List[Post]:
    global _CACHED_POSTS
    if _CACHED_POSTS is None:
        _CACHED_POSTS = await Post.list()
    return _CACHED_POSTS


async def update_posts_cache():
    global _CACHED_POSTS
    _CACHED_POSTS = await Post.list()



