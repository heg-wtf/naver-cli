from naver_cli.models import LocalSearchItem, LocalSearchResponse


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
