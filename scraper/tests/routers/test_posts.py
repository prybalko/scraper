from typing import List
from unittest import mock

from fastapi.testclient import TestClient

from scraper.main import app
from scraper.models.post import Post

client = TestClient(app)

MOCK_POSTS = [
    Post(id=1, title="c_title", url="c_example.com").dict(),
    Post(id=2, title="b_title", url="a_example.com").dict(),
    Post(id=3, title="a_title", url="b_example.com").dict(),
]


@mock.patch.object(Post, "list", return_value=MOCK_POSTS)
class TestPosts:
    @staticmethod
    def assert_posts(given_posts: List[dict], expected_posts: List[dict]):
        assert len(given_posts) == len(expected_posts)
        for given, expected in zip(given_posts, expected_posts):
            g, e = dict(given), dict(expected)
            assert g.pop("created") == e.pop("created").isoformat()
            assert g == e

    def test_with_no_args(self, _):
        response = client.get("/posts")
        assert response.status_code == 200
        self.assert_posts(response.json(), MOCK_POSTS)

    def test_offset(self, _):
        response = client.get("/posts", params=dict(offset=1))
        assert response.status_code == 200
        data = response.json()
        self.assert_posts(data, MOCK_POSTS[1:])

    def test_negative_offset(self, _):
        response = client.get("/posts", params=dict(offset=-1))
        assert response.status_code == 422

    def test_limit(self, _):
        response = client.get("/posts", params=dict(limit=1))
        assert response.status_code == 200
        data = response.json()
        self.assert_posts(data, MOCK_POSTS[:1])

    def test_invalid_limit(self, _):
        response = client.get("/posts", params=dict(limit=-1))
        assert response.status_code == 422
        response = client.get("/posts", params=dict(limit=10000))
        assert response.status_code == 422
        response = client.get("/posts", params=dict(limit="foo"))
        assert response.status_code == 422

    def test_ignore_invalid_order_arg(self, _):
        response = client.get("/posts", params=dict(order="foo"))
        self.assert_posts(response.json(), MOCK_POSTS)

    def test_order(self, _):
        response = client.get("/posts", params=dict(order="title"))
        self.assert_posts(response.json(), MOCK_POSTS[::-1])
