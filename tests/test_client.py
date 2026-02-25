import pytest
from pytest_httpx import HTTPXMock

from naver_cli.client import NaverApiError, NaverClient

from .conftest import (
    SAMPLE_BLOG_RESPONSE,
    SAMPLE_BOOK_RESPONSE,
    SAMPLE_CAFE_RESPONSE,
    SAMPLE_ERROR_RESPONSE,
    SAMPLE_LOCAL_RESPONSE,
    SAMPLE_NEWS_RESPONSE,
    SAMPLE_SHOPPING_RESPONSE,
)


class TestNaverClient:
    def setup_method(self) -> None:
        self.client = NaverClient(
            client_id="test_id",
            client_secret="test_secret",
        )

    def test_search_local_success(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_LOCAL_RESPONSE)

        result = self.client.search_local(query="강남역 맛집")

        assert result.total == 2
        assert len(result.items) == 2
        assert result.items[0].title == "맛집A"
        assert result.items[1].category == "일식"

    def test_search_local_sends_auth_headers(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_LOCAL_RESPONSE)

        self.client.search_local(query="테스트")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.headers["X-Naver-Client-Id"] == "test_id"
        assert request.headers["X-Naver-Client-Secret"] == "test_secret"

    def test_search_local_sends_query_parameters(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_LOCAL_RESPONSE)

        self.client.search_local(query="판교 카페", display=3, start=1, sort="comment")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["query"] == "판교 카페"
        assert request.url.params["display"] == "3"
        assert request.url.params["sort"] == "comment"

    def test_search_local_api_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=400, json=SAMPLE_ERROR_RESPONSE)

        with pytest.raises(NaverApiError) as exception_information:
            self.client.search_local(query="")

        assert exception_information.value.error_code == "SE01"
        assert exception_information.value.status_code == 400


class TestSearchBook:
    def setup_method(self) -> None:
        self.client = NaverClient(client_id="test_id", client_secret="test_secret")

    def test_search_book_success(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_BOOK_RESPONSE)

        result = self.client.search_book(query="파이썬")

        assert result.total == 1
        assert len(result.items) == 1
        assert result.items[0].title == "파이썬 프로그래밍"
        assert result.items[0].author == "홍길동"

    def test_search_book_sends_parameters(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_BOOK_RESPONSE)

        self.client.search_book(query="파이썬", display=20, start=1, sort="date")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["query"] == "파이썬"
        assert request.url.params["display"] == "20"
        assert request.url.params["sort"] == "date"

    def test_search_book_api_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=400, json=SAMPLE_ERROR_RESPONSE)

        with pytest.raises(NaverApiError):
            self.client.search_book(query="")


class TestSearchBlog:
    def setup_method(self) -> None:
        self.client = NaverClient(client_id="test_id", client_secret="test_secret")

    def test_search_blog_success(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_BLOG_RESPONSE)

        result = self.client.search_blog(query="맛집")

        assert result.total == 1
        assert result.items[0].title == "맛집 추천 블로그"
        assert result.items[0].bloggername == "맛집탐험가"

    def test_search_blog_sends_parameters(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_BLOG_RESPONSE)

        self.client.search_blog(query="맛집", display=5, sort="date")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["query"] == "맛집"
        assert request.url.params["sort"] == "date"

    def test_search_blog_api_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=400, json=SAMPLE_ERROR_RESPONSE)

        with pytest.raises(NaverApiError):
            self.client.search_blog(query="")


class TestSearchCafe:
    def setup_method(self) -> None:
        self.client = NaverClient(client_id="test_id", client_secret="test_secret")

    def test_search_cafe_success(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_CAFE_RESPONSE)

        result = self.client.search_cafe(query="카페")

        assert result.total == 1
        assert result.items[0].title == "카페 추천글"
        assert result.items[0].cafename == "맛집카페"

    def test_search_cafe_sends_parameters(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_CAFE_RESPONSE)

        self.client.search_cafe(query="카페", display=15, sort="date")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["query"] == "카페"
        assert request.url.params["display"] == "15"

    def test_search_cafe_api_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=400, json=SAMPLE_ERROR_RESPONSE)

        with pytest.raises(NaverApiError):
            self.client.search_cafe(query="")


class TestSearchNews:
    def setup_method(self) -> None:
        self.client = NaverClient(client_id="test_id", client_secret="test_secret")

    def test_search_news_success(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_NEWS_RESPONSE)

        result = self.client.search_news(query="속보")

        assert result.total == 1
        assert result.items[0].title == "속보 테스트 뉴스"
        assert result.items[0].originallink == "https://news.example.com/original/1"

    def test_search_news_sends_parameters(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_NEWS_RESPONSE)

        self.client.search_news(query="속보", display=30, sort="date")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["query"] == "속보"
        assert request.url.params["display"] == "30"

    def test_search_news_api_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=400, json=SAMPLE_ERROR_RESPONSE)

        with pytest.raises(NaverApiError):
            self.client.search_news(query="")


class TestSearchShopping:
    def setup_method(self) -> None:
        self.client = NaverClient(client_id="test_id", client_secret="test_secret")

    def test_search_shopping_success(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_SHOPPING_RESPONSE)

        result = self.client.search_shopping(query="노트북")

        assert result.total == 1
        assert result.items[0].title == "노트북 프로"
        assert result.items[0].mall_name == "테스트몰"

    def test_search_shopping_sends_parameters(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=SAMPLE_SHOPPING_RESPONSE)

        self.client.search_shopping(query="노트북", display=50, sort="asc")

        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["query"] == "노트북"
        assert request.url.params["display"] == "50"
        assert request.url.params["sort"] == "asc"

    def test_search_shopping_api_error(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=400, json=SAMPLE_ERROR_RESPONSE)

        with pytest.raises(NaverApiError):
            self.client.search_shopping(query="")
