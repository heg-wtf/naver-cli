from typing import Any

import httpx

from naver_cli.config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from naver_cli.models import (
    BlogSearchItem,
    BlogSearchResponse,
    BookSearchItem,
    BookSearchResponse,
    CafeSearchItem,
    CafeSearchResponse,
    LocalSearchItem,
    LocalSearchResponse,
    NewsSearchItem,
    NewsSearchResponse,
    ShoppingSearchItem,
    ShoppingSearchResponse,
)

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

    def _search(
        self,
        endpoint: str,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "sim",
    ) -> dict:
        """공통 검색 API 호출을 수행한다.

        Args:
            endpoint: 검색 API 엔드포인트 (예: "local.json")
            query: 검색어
            display: 검색 결과 출력 건수
            start: 검색 시작 위치
            sort: 정렬 옵션

        Returns:
            API 응답 딕셔너리
        """
        params: dict[str, Any] = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort,
        }

        response = httpx.get(
            f"{BASE_URL}/{endpoint}",
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            body = response.json()
            raise NaverApiError(
                status_code=response.status_code,
                error_code=body.get("errorCode", "UNKNOWN"),
                error_message=body.get("errorMessage", "알 수 없는 오류"),
            )

        return response.json()

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
        data = self._search("local.json", query, display, start, sort)
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

    def search_book(
        self,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "sim",
    ) -> BookSearchResponse:
        """책 검색 API를 호출한다.

        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (1~100)
            start: 검색 시작 위치
            sort: 정렬 옵션 (sim: 정확도순, date: 출간일순, count: 판매량순)

        Returns:
            책 검색 응답 결과
        """
        data = self._search("book.json", query, display, start, sort)
        return BookSearchResponse(
            last_build_date=data.get("lastBuildDate", ""),
            total=data.get("total", 0),
            start=data.get("start", 0),
            display=data.get("display", 0),
            items=[
                BookSearchItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    image=item.get("image", ""),
                    author=item.get("author", ""),
                    discount=item.get("discount", ""),
                    publisher=item.get("publisher", ""),
                    pubdate=item.get("pubdate", ""),
                    isbn=item.get("isbn", ""),
                    description=item.get("description", ""),
                )
                for item in data.get("items", [])
            ],
        )

    def search_blog(
        self,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "sim",
    ) -> BlogSearchResponse:
        """블로그 검색 API를 호출한다.

        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (1~100)
            start: 검색 시작 위치
            sort: 정렬 옵션 (sim: 정확도순, date: 날짜순)

        Returns:
            블로그 검색 응답 결과
        """
        data = self._search("blog.json", query, display, start, sort)
        return BlogSearchResponse(
            last_build_date=data.get("lastBuildDate", ""),
            total=data.get("total", 0),
            start=data.get("start", 0),
            display=data.get("display", 0),
            items=[
                BlogSearchItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    description=item.get("description", ""),
                    bloggername=item.get("bloggername", ""),
                    bloggerlink=item.get("bloggerlink", ""),
                    postdate=item.get("postdate", ""),
                )
                for item in data.get("items", [])
            ],
        )

    def search_cafe(
        self,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "sim",
    ) -> CafeSearchResponse:
        """카페글 검색 API를 호출한다.

        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (1~100)
            start: 검색 시작 위치
            sort: 정렬 옵션 (sim: 정확도순, date: 날짜순)

        Returns:
            카페글 검색 응답 결과
        """
        data = self._search("cafearticle.json", query, display, start, sort)
        return CafeSearchResponse(
            last_build_date=data.get("lastBuildDate", ""),
            total=data.get("total", 0),
            start=data.get("start", 0),
            display=data.get("display", 0),
            items=[
                CafeSearchItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    description=item.get("description", ""),
                    cafename=item.get("cafename", ""),
                    cafeurl=item.get("cafeurl", ""),
                )
                for item in data.get("items", [])
            ],
        )

    def search_news(
        self,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "sim",
    ) -> NewsSearchResponse:
        """뉴스 검색 API를 호출한다.

        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (1~100)
            start: 검색 시작 위치
            sort: 정렬 옵션 (sim: 정확도순, date: 날짜순)

        Returns:
            뉴스 검색 응답 결과
        """
        data = self._search("news.json", query, display, start, sort)
        return NewsSearchResponse(
            last_build_date=data.get("lastBuildDate", ""),
            total=data.get("total", 0),
            start=data.get("start", 0),
            display=data.get("display", 0),
            items=[
                NewsSearchItem(
                    title=item.get("title", ""),
                    originallink=item.get("originallink", ""),
                    link=item.get("link", ""),
                    description=item.get("description", ""),
                    pub_date=item.get("pubDate", ""),
                )
                for item in data.get("items", [])
            ],
        )

    def search_shopping(
        self,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "sim",
    ) -> ShoppingSearchResponse:
        """쇼핑 검색 API를 호출한다.

        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (1~100)
            start: 검색 시작 위치
            sort: 정렬 옵션 (sim: 정확도순, date: 날짜순, asc: 가격낮은순, dsc: 가격높은순)

        Returns:
            쇼핑 검색 응답 결과
        """
        data = self._search("shop.json", query, display, start, sort)
        return ShoppingSearchResponse(
            last_build_date=data.get("lastBuildDate", ""),
            total=data.get("total", 0),
            start=data.get("start", 0),
            display=data.get("display", 0),
            items=[
                ShoppingSearchItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    image=item.get("image", ""),
                    lprice=item.get("lprice", ""),
                    hprice=item.get("hprice", ""),
                    mall_name=item.get("mallName", ""),
                    product_id=item.get("productId", ""),
                    product_type=item.get("productType", ""),
                    brand=item.get("brand", ""),
                    maker=item.get("maker", ""),
                    category1=item.get("category1", ""),
                    category2=item.get("category2", ""),
                    category3=item.get("category3", ""),
                    category4=item.get("category4", ""),
                )
                for item in data.get("items", [])
            ],
        )
