import pytest
from pytest_httpx import HTTPXMock

from naver_cli.client import NaverApiError, NaverClient

from .conftest import SAMPLE_ERROR_RESPONSE, SAMPLE_LOCAL_RESPONSE


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
