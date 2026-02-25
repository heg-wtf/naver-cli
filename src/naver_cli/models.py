import re

from pydantic import BaseModel, ConfigDict, field_validator


class LocalSearchItem(BaseModel):
    """네이버 지역 검색 결과 항목."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    link: str
    category: str
    description: str
    telephone: str
    address: str
    road_address: str = ""
    mapx: int = 0
    mapy: int = 0

    @field_validator("title", mode="before")
    @classmethod
    def strip_html_tags(cls, value: str) -> str:
        """HTML 태그를 제거한다."""
        return re.sub(r"<[^>]+>", "", value)


class LocalSearchResponse(BaseModel):
    """네이버 지역 검색 API 응답."""

    last_build_date: str = ""
    total: int = 0
    start: int = 0
    display: int = 0
    items: list[LocalSearchItem] = []


class BookSearchItem(BaseModel):
    """네이버 책 검색 결과 항목."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    link: str
    image: str = ""
    author: str = ""
    discount: str = ""
    publisher: str = ""
    pubdate: str = ""
    isbn: str = ""
    description: str = ""

    @field_validator("title", mode="before")
    @classmethod
    def strip_html_tags(cls, value: str) -> str:
        """HTML 태그를 제거한다."""
        return re.sub(r"<[^>]+>", "", value)


class BookSearchResponse(BaseModel):
    """네이버 책 검색 API 응답."""

    last_build_date: str = ""
    total: int = 0
    start: int = 0
    display: int = 0
    items: list[BookSearchItem] = []


class BlogSearchItem(BaseModel):
    """네이버 블로그 검색 결과 항목."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    link: str
    description: str = ""
    bloggername: str = ""
    bloggerlink: str = ""
    postdate: str = ""

    @field_validator("title", mode="before")
    @classmethod
    def strip_html_tags(cls, value: str) -> str:
        """HTML 태그를 제거한다."""
        return re.sub(r"<[^>]+>", "", value)


class BlogSearchResponse(BaseModel):
    """네이버 블로그 검색 API 응답."""

    last_build_date: str = ""
    total: int = 0
    start: int = 0
    display: int = 0
    items: list[BlogSearchItem] = []


class CafeSearchItem(BaseModel):
    """네이버 카페글 검색 결과 항목."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    link: str
    description: str = ""
    cafename: str = ""
    cafeurl: str = ""

    @field_validator("title", mode="before")
    @classmethod
    def strip_html_tags(cls, value: str) -> str:
        """HTML 태그를 제거한다."""
        return re.sub(r"<[^>]+>", "", value)


class CafeSearchResponse(BaseModel):
    """네이버 카페글 검색 API 응답."""

    last_build_date: str = ""
    total: int = 0
    start: int = 0
    display: int = 0
    items: list[CafeSearchItem] = []


class NewsSearchItem(BaseModel):
    """네이버 뉴스 검색 결과 항목."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    originallink: str = ""
    link: str = ""
    description: str = ""
    pub_date: str = ""

    @field_validator("title", mode="before")
    @classmethod
    def strip_html_tags(cls, value: str) -> str:
        """HTML 태그를 제거한다."""
        return re.sub(r"<[^>]+>", "", value)


class NewsSearchResponse(BaseModel):
    """네이버 뉴스 검색 API 응답."""

    last_build_date: str = ""
    total: int = 0
    start: int = 0
    display: int = 0
    items: list[NewsSearchItem] = []


class ShoppingSearchItem(BaseModel):
    """네이버 쇼핑 검색 결과 항목."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    link: str = ""
    image: str = ""
    lprice: str = ""
    hprice: str = ""
    mall_name: str = ""
    product_id: str = ""
    product_type: str = ""
    brand: str = ""
    maker: str = ""
    category1: str = ""
    category2: str = ""
    category3: str = ""
    category4: str = ""

    @field_validator("title", mode="before")
    @classmethod
    def strip_html_tags(cls, value: str) -> str:
        """HTML 태그를 제거한다."""
        return re.sub(r"<[^>]+>", "", value)


class ShoppingSearchResponse(BaseModel):
    """네이버 쇼핑 검색 API 응답."""

    last_build_date: str = ""
    total: int = 0
    start: int = 0
    display: int = 0
    items: list[ShoppingSearchItem] = []
