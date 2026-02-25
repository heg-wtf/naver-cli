from unittest.mock import patch

from typer.testing import CliRunner

from naver_cli.main import app
from naver_cli.models import BlogSearchItem, BlogSearchResponse

runner = CliRunner()


def _make_search_response() -> BlogSearchResponse:
    return BlogSearchResponse(
        last_build_date="Wed, 25 Feb 2026 08:00:00 +0900",
        total=1,
        start=1,
        display=1,
        items=[
            BlogSearchItem(
                title="맛집 추천 블로그",
                link="https://blog.example.com/1",
                description="강남역 맛집 리뷰",
                bloggername="맛집탐험가",
                bloggerlink="https://blog.example.com",
                postdate="20260225",
            )
        ],
    )


class TestBlogSearchCommand:
    @patch("naver_cli.commands.blog.validate_credentials", return_value=True)
    @patch("naver_cli.commands.blog.NaverClient")
    def test_search_success(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_blog.return_value = _make_search_response()

        result = runner.invoke(app, ["blog", "search", "맛집"])

        assert result.exit_code == 0
        assert "맛집 추천 블로그" in result.output
        assert "맛집탐험가" in result.output

    @patch("naver_cli.commands.blog.validate_credentials", return_value=True)
    @patch("naver_cli.commands.blog.NaverClient")
    def test_search_with_options(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_blog.return_value = _make_search_response()

        result = runner.invoke(
            app,
            ["blog", "search", "맛집", "--display", "5", "--sort", "date"],
        )

        assert result.exit_code == 0
        mock_client_class.return_value.search_blog.assert_called_once_with(
            query="맛집",
            display=5,
            start=1,
            sort="date",
        )

    @patch("naver_cli.commands.blog.validate_credentials", return_value=False)
    def test_search_without_credentials(self, mock_validate) -> None:
        result = runner.invoke(app, ["blog", "search", "테스트"])

        assert result.exit_code == 1
        assert "NAVER_CLIENT_ID" in result.output

    @patch("naver_cli.commands.blog.validate_credentials", return_value=True)
    @patch("naver_cli.commands.blog.NaverClient")
    def test_search_no_results(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_blog.return_value = BlogSearchResponse()

        result = runner.invoke(app, ["blog", "search", "없는내용"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestBlogOutputFormat:
    @patch("naver_cli.commands.blog.validate_credentials", return_value=True)
    @patch("naver_cli.commands.blog.NaverClient")
    def test_format_text(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_blog.return_value = _make_search_response()

        result = runner.invoke(app, ["blog", "search", "테스트", "--format", "text"])

        assert result.exit_code == 0
        assert "맛집 추천 블로그" in result.output

    @patch("naver_cli.commands.blog.validate_credentials", return_value=True)
    @patch("naver_cli.commands.blog.NaverClient")
    def test_format_markdown(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_blog.return_value = _make_search_response()

        result = runner.invoke(app, ["blog", "search", "테스트", "--format", "markdown"])

        assert result.exit_code == 0
        assert "| 제목 | 블로거 | 작성일 | 링크 |" in result.output
        assert "| 맛집 추천 블로그 |" in result.output

    @patch("naver_cli.commands.blog.validate_credentials", return_value=True)
    @patch("naver_cli.commands.blog.NaverClient")
    def test_format_json(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_blog.return_value = _make_search_response()

        result = runner.invoke(app, ["blog", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"title": "맛집 추천 블로그"' in result.output
        assert '"bloggername": "맛집탐험가"' in result.output
        assert '"total": 1' in result.output
