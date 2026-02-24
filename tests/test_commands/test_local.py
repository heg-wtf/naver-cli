from unittest.mock import patch

from typer.testing import CliRunner

from naver_cli.main import app
from naver_cli.models import LocalSearchItem, LocalSearchResponse

runner = CliRunner()


def _make_search_response() -> LocalSearchResponse:
    return LocalSearchResponse(
        last_build_date="Wed, 25 Feb 2026 08:00:00 +0900",
        total=1,
        start=1,
        display=1,
        items=[
            LocalSearchItem(
                title="테스트 맛집",
                link="https://example.com",
                category="한식",
                description="맛있는 곳",
                telephone="02-1234-5678",
                address="서울특별시 강남구",
                road_address="서울특별시 강남구 역삼로 100",
            )
        ],
    )


class TestLocalSearchCommand:
    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_search_success(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = _make_search_response()

        result = runner.invoke(app, ["local", "search", "강남역 맛집"])

        assert result.exit_code == 0
        assert "테스트 맛집" in result.output
        assert "한식" in result.output

    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_search_with_options(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = _make_search_response()

        result = runner.invoke(
            app,
            ["local", "search", "판교 카페", "--display", "3", "--sort", "comment"],
        )

        assert result.exit_code == 0
        mock_client_class.return_value.search_local.assert_called_once_with(
            query="판교 카페",
            display=3,
            start=1,
            sort="comment",
        )

    @patch("naver_cli.commands.local.validate_credentials", return_value=False)
    def test_search_without_credentials(self, mock_validate) -> None:
        result = runner.invoke(app, ["local", "search", "테스트"])

        assert result.exit_code == 1
        assert "NAVER_CLIENT_ID" in result.output

    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_search_no_results(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = LocalSearchResponse()

        result = runner.invoke(app, ["local", "search", "없는장소"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestOutputFormat:
    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_format_text(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = _make_search_response()

        result = runner.invoke(app, ["local", "search", "테스트", "--format", "text"])

        assert result.exit_code == 0
        assert "테스트 맛집" in result.output
        assert "한식" in result.output

    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_format_markdown(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = _make_search_response()

        result = runner.invoke(app, ["local", "search", "테스트", "--format", "markdown"])

        assert result.exit_code == 0
        assert "| 이름 | 카테고리 | 도로명 주소 | 전화번호 |" in result.output
        assert "|------|----------|-------------|----------|" in result.output
        assert "| 테스트 맛집 |" in result.output

    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_format_json(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = _make_search_response()

        result = runner.invoke(app, ["local", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"title": "테스트 맛집"' in result.output
        assert '"category": "한식"' in result.output
        assert '"total": 1' in result.output

    @patch("naver_cli.commands.local.validate_credentials", return_value=True)
    @patch("naver_cli.commands.local.NaverClient")
    def test_format_json_contains_all_fields(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_local.return_value = _make_search_response()

        result = runner.invoke(app, ["local", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"link"' in result.output
        assert '"description"' in result.output
        assert '"mapx"' in result.output
        assert '"mapy"' in result.output
