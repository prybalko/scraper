from typing import List, Optional

from fastapi_contrib.db.models import MongoDBTimeStampedModel


class Post(MongoDBTimeStampedModel):
    __CACHED_POSTS: Optional[List["Post"]] = None
    id: int
    title: str
    url: str

    class Meta:
        collection = "posts"

    @classmethod
    async def all(cls) -> List["Post"]:
        if cls.__CACHED_POSTS is None:
            cls.__CACHED_POSTS = await Post.list()
        return cls.__CACHED_POSTS

    @classmethod
    async def update_cache(cls):
        cls.__CACHED_POSTS = await cls.list()
