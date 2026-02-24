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

SAMPLE_ERROR_RESPONSE = {
    "errorCode": "SE01",
    "errorMessage": "Incorrect query request",
}


@pytest.fixture
def sample_local_response() -> dict:
    return SAMPLE_LOCAL_RESPONSE


@pytest.fixture
def sample_error_response() -> dict:
    return SAMPLE_ERROR_RESPONSE
