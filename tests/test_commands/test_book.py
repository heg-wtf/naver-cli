from unittest.mock import patch

from typer.testing import CliRunner

from naver_cli.main import app
from naver_cli.models import BookSearchItem, BookSearchResponse

runner = CliRunner()


def _make_search_response() -> BookSearchResponse:
    return BookSearchResponse(
        last_build_date="Wed, 25 Feb 2026 08:00:00 +0900",
        total=1,
        start=1,
        display=1,
        items=[
            BookSearchItem(
                title="파이썬 프로그래밍",
                link="https://example.com/book1",
                image="https://example.com/book1.jpg",
                author="홍길동",
                discount="25000",
                publisher="한빛미디어",
                pubdate="20250101",
                isbn="1234567890123",
                description="파이썬 입문서",
            )
        ],
    )


class TestBookSearchCommand:
    @patch("naver_cli.commands.book.validate_credentials", return_value=True)
    @patch("naver_cli.commands.book.NaverClient")
    def test_search_success(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_book.return_value = _make_search_response()

        result = runner.invoke(app, ["book", "search", "파이썬"])

        assert result.exit_code == 0
        assert "파이썬 프로그래밍" in result.output
        assert "홍길동" in result.output

    @patch("naver_cli.commands.book.validate_credentials", return_value=True)
    @patch("naver_cli.commands.book.NaverClient")
    def test_search_with_options(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_book.return_value = _make_search_response()

        result = runner.invoke(
            app,
            ["book", "search", "파이썬", "--display", "20", "--sort", "date"],
        )

        assert result.exit_code == 0
        mock_client_class.return_value.search_book.assert_called_once_with(
            query="파이썬",
            display=20,
            start=1,
            sort="date",
        )

    @patch("naver_cli.commands.book.validate_credentials", return_value=False)
    def test_search_without_credentials(self, mock_validate) -> None:
        result = runner.invoke(app, ["book", "search", "테스트"])

        assert result.exit_code == 1
        assert "NAVER_CLIENT_ID" in result.output

    @patch("naver_cli.commands.book.validate_credentials", return_value=True)
    @patch("naver_cli.commands.book.NaverClient")
    def test_search_no_results(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_book.return_value = BookSearchResponse()

        result = runner.invoke(app, ["book", "search", "없는책"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestBookOutputFormat:
    @patch("naver_cli.commands.book.validate_credentials", return_value=True)
    @patch("naver_cli.commands.book.NaverClient")
    def test_format_text(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_book.return_value = _make_search_response()

        result = runner.invoke(app, ["book", "search", "테스트", "--format", "text"])

        assert result.exit_code == 0
        assert "파이썬 프로그래밍" in result.output
        assert "홍길동" in result.output

    @patch("naver_cli.commands.book.validate_credentials", return_value=True)
    @patch("naver_cli.commands.book.NaverClient")
    def test_format_markdown(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_book.return_value = _make_search_response()

        result = runner.invoke(app, ["book", "search", "테스트", "--format", "markdown"])

        assert result.exit_code == 0
        assert "| 제목 | 저자 | 출판사 | 가격 | ISBN |" in result.output
        assert "| 파이썬 프로그래밍 |" in result.output

    @patch("naver_cli.commands.book.validate_credentials", return_value=True)
    @patch("naver_cli.commands.book.NaverClient")
    def test_format_json(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_book.return_value = _make_search_response()

        result = runner.invoke(app, ["book", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"title": "파이썬 프로그래밍"' in result.output
        assert '"author": "홍길동"' in result.output
        assert '"total": 1' in result.output
