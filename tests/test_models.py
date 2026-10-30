from naver_cli.models import (
    BlogSearchItem,
    BlogSearchResponse,
    CafeSearchItem,
    CafeSearchResponse,
    LocalSearchItem,
    LocalSearchResponse,
    NewsSearchItem,
    NewsSearchResponse,
)


class TestLocalSearchItem:
    def test_strip_html_tags_from_title(self) -> None:
        item = LocalSearchItem(
            title="<b>맛집</b>A",
            link="",
            category="한식",
            description="",
            telephone="",
            address="서울",
        )
        assert item.title == "맛집A"

    def test_strip_multiple_html_tags(self) -> None:
        item = LocalSearchItem(
            title="<b>강남</b> <i>맛집</i>",
            link="",
            category="",
            description="",
            telephone="",
            address="",
        )
        assert item.title == "강남 맛집"

    def test_no_html_tags_unchanged(self) -> None:
        item = LocalSearchItem(
            title="일반 텍스트",
            link="",
            category="",
            description="",
            telephone="",
            address="",
        )
        assert item.title == "일반 텍스트"


class TestLocalSearchResponse:
    def test_parse_response(self, sample_local_response: dict) -> None:
        data = sample_local_response
        response = LocalSearchResponse(
            last_build_date=data["lastBuildDate"],
            total=data["total"],
            start=data["start"],
            display=data["display"],
            items=[
                LocalSearchItem(
                    title=item["title"],
                    link=item["link"],
                    category=item["category"],
                    description=item["description"],
                    telephone=item["telephone"],
                    address=item["address"],
                    road_address=item.get("roadAddress", ""),
                    mapx=item.get("mapx", 0),
                    mapy=item.get("mapy", 0),
                )
                for item in data["items"]
            ],
        )
        assert response.total == 2
        assert len(response.items) == 2
        assert response.items[0].title == "맛집A"
        assert response.items[0].road_address == "서울특별시 강남구 역삼로 100"

    def test_empty_response(self) -> None:
        response = LocalSearchResponse()
        assert response.total == 0
        assert response.items == []


class TestBlogSearchItem:
    def test_strip_html_tags_from_title(self) -> None:
        item = BlogSearchItem(
            title="<b>맛집</b> 추천",
            link="",
        )
        assert item.title == "맛집 추천"

    def test_all_fields(self) -> None:
        item = BlogSearchItem(
            title="블로그 글",
            link="https://example.com",
            description="설명",
            bloggername="블로거",
            bloggerlink="https://blog.example.com",
            postdate="20260225",
        )
        assert item.bloggername == "블로거"
        assert item.postdate == "20260225"


class TestBlogSearchResponse:
    def test_parse_response(self, sample_blog_response: dict) -> None:
        data = sample_blog_response
        response = BlogSearchResponse(
            total=data["total"],
            items=[BlogSearchItem(**item) for item in data["items"]],
        )
        assert response.total == 1
        assert response.items[0].title == "맛집 추천 블로그"

    def test_empty_response(self) -> None:
        response = BlogSearchResponse()
        assert response.total == 0
        assert response.items == []


class TestCafeSearchItem:
    def test_strip_html_tags_from_title(self) -> None:
        item = CafeSearchItem(
            title="<b>카페</b> 추천",
            link="",
        )
        assert item.title == "카페 추천"

    def test_all_fields(self) -> None:
        item = CafeSearchItem(
            title="카페글",
            link="https://example.com",
            description="설명",
            cafename="카페이름",
            cafeurl="https://cafe.example.com",
        )
        assert item.cafename == "카페이름"
        assert item.cafeurl == "https://cafe.example.com"


class TestCafeSearchResponse:
    def test_parse_response(self, sample_cafe_response: dict) -> None:
        data = sample_cafe_response
        response = CafeSearchResponse(
            total=data["total"],
            items=[CafeSearchItem(**item) for item in data["items"]],
        )
        assert response.total == 1
        assert response.items[0].title == "카페 추천글"

    def test_empty_response(self) -> None:
        response = CafeSearchResponse()
        assert response.total == 0
        assert response.items == []


class TestNewsSearchItem:
    def test_strip_html_tags_from_title(self) -> None:
        item = NewsSearchItem(
            title="<b>속보</b> 뉴스",
        )
        assert item.title == "속보 뉴스"

    def test_all_fields(self) -> None:
        item = NewsSearchItem(
            title="뉴스 제목",
            originallink="https://news.example.com/original",
            link="https://news.example.com",
            description="뉴스 내용",
            pub_date="Wed, 25 Feb 2026 08:00:00 +0900",
        )
        assert item.originallink == "https://news.example.com/original"
        assert item.pub_date == "Wed, 25 Feb 2026 08:00:00 +0900"


class TestNewsSearchResponse:
    def test_parse_response(self, sample_news_response: dict) -> None:
        data = sample_news_response
        response = NewsSearchResponse(
            total=data["total"],
            items=[
                NewsSearchItem(
                    title=item["title"],
                    originallink=item.get("originallink", ""),
                    link=item.get("link", ""),
                    description=item.get("description", ""),
                    pub_date=item.get("pubDate", ""),
                )
                for item in data["items"]
            ],
        )
        assert response.total == 1
        assert response.items[0].title == "속보 테스트 뉴스"

    def test_empty_response(self) -> None:
        response = NewsSearchResponse()
        assert response.total == 0
        assert response.items == []
