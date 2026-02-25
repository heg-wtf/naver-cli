from unittest.mock import patch

from typer.testing import CliRunner

from naver_cli.main import app
from naver_cli.models import CafeSearchItem, CafeSearchResponse

runner = CliRunner()


def _make_search_response() -> CafeSearchResponse:
    return CafeSearchResponse(
        last_build_date="Wed, 25 Feb 2026 08:00:00 +0900",
        total=1,
        start=1,
        display=1,
        items=[
            CafeSearchItem(
                title="카페 추천글",
                link="https://cafe.example.com/1",
                description="카페 추천 게시글",
                cafename="맛집카페",
                cafeurl="https://cafe.example.com",
            )
        ],
    )


class TestCafeSearchCommand:
    @patch("naver_cli.commands.cafe.validate_credentials", return_value=True)
    @patch("naver_cli.commands.cafe.NaverClient")
    def test_search_success(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_cafe.return_value = _make_search_response()

        result = runner.invoke(app, ["cafe", "search", "카페"])

        assert result.exit_code == 0
        assert "카페 추천글" in result.output
        assert "맛집카페" in result.output

    @patch("naver_cli.commands.cafe.validate_credentials", return_value=True)
    @patch("naver_cli.commands.cafe.NaverClient")
    def test_search_with_options(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_cafe.return_value = _make_search_response()

        result = runner.invoke(
            app,
            ["cafe", "search", "카페", "--display", "15", "--sort", "date"],
        )

        assert result.exit_code == 0
        mock_client_class.return_value.search_cafe.assert_called_once_with(
            query="카페",
            display=15,
            start=1,
            sort="date",
        )

    @patch("naver_cli.commands.cafe.validate_credentials", return_value=False)
    def test_search_without_credentials(self, mock_validate) -> None:
        result = runner.invoke(app, ["cafe", "search", "테스트"])

        assert result.exit_code == 1
        assert "NAVER_CLIENT_ID" in result.output

    @patch("naver_cli.commands.cafe.validate_credentials", return_value=True)
    @patch("naver_cli.commands.cafe.NaverClient")
    def test_search_no_results(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_cafe.return_value = CafeSearchResponse()

        result = runner.invoke(app, ["cafe", "search", "없는내용"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestCafeOutputFormat:
    @patch("naver_cli.commands.cafe.validate_credentials", return_value=True)
    @patch("naver_cli.commands.cafe.NaverClient")
    def test_format_text(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_cafe.return_value = _make_search_response()

        result = runner.invoke(app, ["cafe", "search", "테스트", "--format", "text"])

        assert result.exit_code == 0
        assert "카페 추천글" in result.output

    @patch("naver_cli.commands.cafe.validate_credentials", return_value=True)
    @patch("naver_cli.commands.cafe.NaverClient")
    def test_format_markdown(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_cafe.return_value = _make_search_response()

        result = runner.invoke(app, ["cafe", "search", "테스트", "--format", "markdown"])

        assert result.exit_code == 0
        assert "| 제목 | 카페명 | 링크 |" in result.output
        assert "| 카페 추천글 |" in result.output

    @patch("naver_cli.commands.cafe.validate_credentials", return_value=True)
    @patch("naver_cli.commands.cafe.NaverClient")
    def test_format_json(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_cafe.return_value = _make_search_response()

        result = runner.invoke(app, ["cafe", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"title": "카페 추천글"' in result.output
        assert '"cafename": "맛집카페"' in result.output
        assert '"total": 1' in result.output
