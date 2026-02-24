import httpx

from naver_cli.config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from naver_cli.models import LocalSearchItem, LocalSearchResponse

BASE_URL = "https://openapi.naver.com/v1/search"


class NaverApiError(Exception):
    """네이버 API 호출 실패 시 발생하는 예외."""

    def __init__(self, status_code: int, error_code: str, error_message: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(f"[{error_code}] {error_message}")


class NaverClient:
    """네이버 오픈 API 클라이언트."""

    def __init__(
        self,
        client_id: str = NAVER_CLIENT_ID,
        client_secret: str = NAVER_CLIENT_SECRET,
    ) -> None:
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }

    def search_local(
        self,
        query: str,
        display: int = 5,
        start: int = 1,
        sort: str = "random",
    ) -> LocalSearchResponse:
        """지역 검색 API를 호출한다.

        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (1~5)
            start: 검색 시작 위치 (1~1)
            sort: 정렬 옵션 (random: 정확도순, comment: 리뷰순)

        Returns:
            지역 검색 응답 결과
        """
        response = httpx.get(
            f"{BASE_URL}/local.json",
            headers=self.headers,
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
        )

        if response.status_code != 200:
            body = response.json()
            raise NaverApiError(
                status_code=response.status_code,
                error_code=body.get("errorCode", "UNKNOWN"),
                error_message=body.get("errorMessage", "알 수 없는 오류"),
            )

        data = response.json()
        return LocalSearchResponse(
            last_build_date=data.get("lastBuildDate", ""),
            total=data.get("total", 0),
            start=data.get("start", 0),
            display=data.get("display", 0),
            items=[
                LocalSearchItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    category=item.get("category", ""),
                    description=item.get("description", ""),
                    telephone=item.get("telephone", ""),
                    address=item.get("address", ""),
                    road_address=item.get("roadAddress", ""),
                    mapx=item.get("mapx", 0),
                    mapy=item.get("mapy", 0),
                )
                for item in data.get("items", [])
            ],
        )
