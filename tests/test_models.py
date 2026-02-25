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


class TestBookSearchItem:
    def test_strip_html_tags_from_title(self) -> None:
        item = BookSearchItem(
            title="<b>파이썬</b> 프로그래밍",
            link="",
        )
        assert item.title == "파이썬 프로그래밍"

    def test_all_fields(self) -> None:
        item = BookSearchItem(
            title="테스트 책",
            link="https://example.com",
            image="https://example.com/img.jpg",
            author="저자",
            discount="25000",
            publisher="출판사",
            pubdate="20250101",
            isbn="1234567890123",
            description="설명",
        )
        assert item.author == "저자"
        assert item.publisher == "출판사"
        assert item.isbn == "1234567890123"


class TestBookSearchResponse:
    def test_parse_response(self, sample_book_response: dict) -> None:
        data = sample_book_response
        response = BookSearchResponse(
            total=data["total"],
            items=[BookSearchItem(**item) for item in data["items"]],
        )
        assert response.total == 1
        assert response.items[0].title == "파이썬 프로그래밍"
        assert response.items[0].author == "홍길동"

    def test_empty_response(self) -> None:
        response = BookSearchResponse()
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


class TestShoppingSearchItem:
    def test_strip_html_tags_from_title(self) -> None:
        item = ShoppingSearchItem(
            title="<b>노트북</b> 프로",
        )
        assert item.title == "노트북 프로"

    def test_all_fields(self) -> None:
        item = ShoppingSearchItem(
            title="상품",
            link="https://example.com",
            lprice="1500000",
            hprice="2000000",
            mall_name="몰",
            brand="브랜드",
            maker="메이커",
            category1="카테고리1",
        )
        assert item.lprice == "1500000"
        assert item.mall_name == "몰"
        assert item.brand == "브랜드"


class TestShoppingSearchResponse:
    def test_parse_response(self, sample_shopping_response: dict) -> None:
        data = sample_shopping_response
        response = ShoppingSearchResponse(
            total=data["total"],
            items=[
                ShoppingSearchItem(
                    title=item["title"],
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
                for item in data["items"]
            ],
        )
        assert response.total == 1
        assert response.items[0].title == "노트북 프로"
        assert response.items[0].mall_name == "테스트몰"

    def test_empty_response(self) -> None:
        response = ShoppingSearchResponse()
        assert response.total == 0
        assert response.items == []
