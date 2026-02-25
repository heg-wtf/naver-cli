from unittest.mock import patch

from typer.testing import CliRunner

from naver_cli.main import app
from naver_cli.models import ShoppingSearchItem, ShoppingSearchResponse

runner = CliRunner()


def _make_search_response() -> ShoppingSearchResponse:
    return ShoppingSearchResponse(
        last_build_date="Wed, 25 Feb 2026 08:00:00 +0900",
        total=1,
        start=1,
        display=1,
        items=[
            ShoppingSearchItem(
                title="노트북 프로",
                link="https://shop.example.com/1",
                image="https://shop.example.com/1.jpg",
                lprice="1500000",
                hprice="2000000",
                mall_name="테스트몰",
                product_id="12345",
                product_type="1",
                brand="테스트브랜드",
                maker="테스트메이커",
                category1="디지털/가전",
                category2="노트북",
            )
        ],
    )


class TestShoppingSearchCommand:
    @patch("naver_cli.commands.shopping.validate_credentials", return_value=True)
    @patch("naver_cli.commands.shopping.NaverClient")
    def test_search_success(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_shopping.return_value = _make_search_response()

        result = runner.invoke(app, ["shopping", "search", "노트북"])

        assert result.exit_code == 0
        assert "노트북 프로" in result.output
        assert "테스트몰" in result.output

    @patch("naver_cli.commands.shopping.validate_credentials", return_value=True)
    @patch("naver_cli.commands.shopping.NaverClient")
    def test_search_with_options(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_shopping.return_value = _make_search_response()

        result = runner.invoke(
            app,
            ["shopping", "search", "노트북", "--display", "50", "--sort", "asc"],
        )

        assert result.exit_code == 0
        mock_client_class.return_value.search_shopping.assert_called_once_with(
            query="노트북",
            display=50,
            start=1,
            sort="asc",
        )

    @patch("naver_cli.commands.shopping.validate_credentials", return_value=False)
    def test_search_without_credentials(self, mock_validate) -> None:
        result = runner.invoke(app, ["shopping", "search", "테스트"])

        assert result.exit_code == 1
        assert "NAVER_CLIENT_ID" in result.output

    @patch("naver_cli.commands.shopping.validate_credentials", return_value=True)
    @patch("naver_cli.commands.shopping.NaverClient")
    def test_search_no_results(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_shopping.return_value = ShoppingSearchResponse()

        result = runner.invoke(app, ["shopping", "search", "없는상품"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestShoppingOutputFormat:
    @patch("naver_cli.commands.shopping.validate_credentials", return_value=True)
    @patch("naver_cli.commands.shopping.NaverClient")
    def test_format_text(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_shopping.return_value = _make_search_response()

        result = runner.invoke(app, ["shopping", "search", "테스트", "--format", "text"])

        assert result.exit_code == 0
        assert "노트북 프로" in result.output
        assert "테스트몰" in result.output

    @patch("naver_cli.commands.shopping.validate_credentials", return_value=True)
    @patch("naver_cli.commands.shopping.NaverClient")
    def test_format_markdown(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_shopping.return_value = _make_search_response()

        result = runner.invoke(app, ["shopping", "search", "테스트", "--format", "markdown"])

        assert result.exit_code == 0
        assert "| 상품명 | 최저가 | 쇼핑몰 | 브랜드 |" in result.output
        assert "| 노트북 프로 |" in result.output

    @patch("naver_cli.commands.shopping.validate_credentials", return_value=True)
    @patch("naver_cli.commands.shopping.NaverClient")
    def test_format_json(self, mock_client_class, mock_validate) -> None:
        mock_client_class.return_value.search_shopping.return_value = _make_search_response()

        result = runner.invoke(app, ["shopping", "search", "테스트", "--format", "json"])

        assert result.exit_code == 0
        assert '"title": "노트북 프로"' in result.output
        assert '"mall_name": "테스트몰"' in result.output
        assert '"total": 1' in result.output
