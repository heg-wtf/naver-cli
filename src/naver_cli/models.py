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
