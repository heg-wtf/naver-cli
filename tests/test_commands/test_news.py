from unittest.mock import patch

from typer.testing import CliRunner

from naver_cli.main import app
from naver_cli.models import NewsSearchItem, NewsSearchResponse

runner = CliRunner()


def _make_search_response() -> NewsSearchResponse:
    return NewsSearchResponse(
        last_build_date="Wed, 25 Feb 2026 08:00:00 +0900",
        total=1,
        start=1,
        display=1,
        items=[
            NewsSearchItem(
                title="속보 테스트 뉴스",
                originallink="https://news.example.com/original/1",
                link="https://news.example.com/1",
                description="테스트 뉴스 내용",
                pub_date="Wed, 25 Feb 2026 08:00:00 +0900",
            )
        ],
    )


class TestNewsSearchCommand:
    @patch("naver_cli.commands.news.validate_credentials", return_value=True)
    @patch("naver_cli.commands.news.NaverClient")
    def test_search_success(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_news.return_value = _make_search_response()

        result = runner.invoke(app, ["news", "search", "속보"])

        assert result.exit_code == 0
        assert "속보 테스트 뉴스" in result.output

    @patch("naver_cli.commands.news.validate_credentials", return_value=True)
    @patch("naver_cli.commands.news.NaverClient")
    def test_search_with_options(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_news.return_value = _make_search_response()

        result = runner.invoke(
            app,
            ["news", "search", "속보", "--display", "30", "--sort", "date"],
        )

        assert result.exit_code == 0
        mock_client_class.return_value.search_news.assert_called_once_with(
            query="속보",
            display=30,
            start=1,
            sort="date",
        )

    @patch("naver_cli.commands.news.validate_credentials", return_value=False)
    def test_search_without_credentials(self, mock_validate) -> None:
        result = runner.invoke(app, ["news", "search", "테스트"])

        assert result.exit_code == 1
        assert "NAVER_CLIENT_ID" in result.output

    @patch("naver_cli.commands.news.validate_credentials", return_value=True)
    @patch("naver_cli.commands.news.NaverClient")
    def test_search_no_results(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_news.return_value = NewsSearchResponse()

        result = runner.invoke(app, ["news", "search", "없는뉴스"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestNewsOutputFormat:
    @patch("naver_cli.commands.news.validate_credentials", return_value=True)
    @patch("naver_cli.commands.news.NaverClient")
    def test_format_text(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_news.return_value = _make_search_response()

        result = runner.invoke(app, ["news", "search", "테스트", "--format", "text"])

        assert result.exit_code == 0
        assert "속보 테스트 뉴스" in result.output

    @patch("naver_cli.commands.news.validate_credentials", return_value=True)
    @patch("naver_cli.commands.news.NaverClient")
    def test_format_markdown(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_news.return_value = _make_search_response()

        result = runner.invoke(app, ["news", "search", "테스트", "--format", "markdown"])

        assert result.exit_code == 0
        assert "| 제목 | 출처링크 | 발행일 |" in result.output
        assert "| 속보 테스트 뉴스 |" in result.output

    @patch("naver_cli.commands.news.validate_credentials", return_value=True)
    @patch("naver_cli.commands.news.NaverClient")
    def test_format_json(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_news.return_value = _make_search_response()

        result = runner.invoke(app, ["news", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"title": "속보 테스트 뉴스"' in result.output
        assert '"total": 1' in result.output
