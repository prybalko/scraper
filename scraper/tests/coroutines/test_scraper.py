import asyncio
import pathlib
from unittest import mock
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from scraper.coroutines.scraper import check_new_posts
from scraper.main import app
from scraper.models.post import Post

client = TestClient(app)

with open(
    f"{pathlib.Path(__file__).parent.absolute()}/data/hackernews.html", "rb"
) as f:
    MOCK_HACKERNEWS = f.read()


class TestScraper:
    @mock.patch.object(Post, "delete")
    @mock.patch.object(Post, "update_cache")
    @mock.patch("scraper.coroutines.scraper.read_url", return_value=MOCK_HACKERNEWS)
    @mock.patch("scraper.coroutines.scraper.Post.save", return_value=1)
    def test_scraper(
        self, mock_save, mock_read: AsyncMock, mock_update_cache, mock_delete
    ):
        asyncio.run(check_new_posts())

        mock_read.assert_called_with("https://news.ycombinator.com/")
        mock_delete.assert_called_once()
        mock_update_cache.assert_called_once()
        assert mock_save.call_count == 30
