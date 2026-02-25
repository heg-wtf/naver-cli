import pytest

SAMPLE_LOCAL_RESPONSE = {
    "lastBuildDate": "Wed, 25 Feb 2026 08:00:00 +0900",
    "total": 2,
    "start": 1,
    "display": 2,
    "items": [
        {
            "title": "<b>맛집</b>A",
            "link": "https://example.com/a",
            "category": "한식",
            "description": "맛있는 한식당",
            "telephone": "02-1234-5678",
            "address": "서울특별시 강남구 역삼동 123",
            "roadAddress": "서울특별시 강남구 역삼로 100",
            "mapx": 127028283,
            "mapy": 37497942,
        },
        {
            "title": "맛집B",
            "link": "https://example.com/b",
            "category": "일식",
            "description": "맛있는 일식당",
            "telephone": "02-8765-4321",
            "address": "서울특별시 강남구 역삼동 456",
            "roadAddress": "서울특별시 강남구 테헤란로 200",
            "mapx": 127029000,
            "mapy": 37498000,
        },
    ],
}

SAMPLE_BOOK_RESPONSE = {
    "lastBuildDate": "Wed, 25 Feb 2026 08:00:00 +0900",
    "total": 1,
    "start": 1,
    "display": 1,
    "items": [
        {
            "title": "<b>파이썬</b> 프로그래밍",
            "link": "https://example.com/book1",
            "image": "https://example.com/book1.jpg",
            "author": "홍길동",
            "discount": "25000",
            "publisher": "한빛미디어",
            "pubdate": "20250101",
            "isbn": "1234567890123",
            "description": "파이썬 입문서",
        },
    ],
}

SAMPLE_BLOG_RESPONSE = {
    "lastBuildDate": "Wed, 25 Feb 2026 08:00:00 +0900",
    "total": 1,
    "start": 1,
    "display": 1,
    "items": [
        {
            "title": "<b>맛집</b> 추천 블로그",
            "link": "https://blog.example.com/1",
            "description": "강남역 맛집 리뷰",
            "bloggername": "맛집탐험가",
            "bloggerlink": "https://blog.example.com",
            "postdate": "20260225",
        },
    ],
}

SAMPLE_CAFE_RESPONSE = {
    "lastBuildDate": "Wed, 25 Feb 2026 08:00:00 +0900",
    "total": 1,
    "start": 1,
    "display": 1,
    "items": [
        {
            "title": "<b>카페</b> 추천글",
            "link": "https://cafe.example.com/1",
            "description": "카페 추천 게시글",
            "cafename": "맛집카페",
            "cafeurl": "https://cafe.example.com",
        },
    ],
}

SAMPLE_NEWS_RESPONSE = {
    "lastBuildDate": "Wed, 25 Feb 2026 08:00:00 +0900",
    "total": 1,
    "start": 1,
    "display": 1,
    "items": [
        {
            "title": "<b>속보</b> 테스트 뉴스",
            "originallink": "https://news.example.com/original/1",
            "link": "https://news.example.com/1",
            "description": "테스트 뉴스 내용",
            "pubDate": "Wed, 25 Feb 2026 08:00:00 +0900",
        },
    ],
}

SAMPLE_SHOPPING_RESPONSE = {
    "lastBuildDate": "Wed, 25 Feb 2026 08:00:00 +0900",
    "total": 1,
    "start": 1,
    "display": 1,
    "items": [
        {
            "title": "<b>노트북</b> 프로",
            "link": "https://shop.example.com/1",
            "image": "https://shop.example.com/1.jpg",
            "lprice": "1500000",
            "hprice": "2000000",
            "mallName": "테스트몰",
            "productId": "12345",
            "productType": "1",
            "brand": "테스트브랜드",
            "maker": "테스트메이커",
            "category1": "디지털/가전",
            "category2": "노트북",
            "category3": "",
            "category4": "",
        },
    ],
}

SAMPLE_ERROR_RESPONSE = {
    "errorCode": "SE01",
    "errorMessage": "Incorrect query request",
}


@pytest.fixture
def sample_local_response() -> dict:
    return SAMPLE_LOCAL_RESPONSE


@pytest.fixture
def sample_book_response() -> dict:
    return SAMPLE_BOOK_RESPONSE


@pytest.fixture
def sample_blog_response() -> dict:
    return SAMPLE_BLOG_RESPONSE


@pytest.fixture
def sample_cafe_response() -> dict:
    return SAMPLE_CAFE_RESPONSE


@pytest.fixture
def sample_news_response() -> dict:
    return SAMPLE_NEWS_RESPONSE


@pytest.fixture
def sample_shopping_response() -> dict:
    return SAMPLE_SHOPPING_RESPONSE


@pytest.fixture
def sample_error_response() -> dict:
    return SAMPLE_ERROR_RESPONSE
