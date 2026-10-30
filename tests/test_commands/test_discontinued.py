"""Naver ended the Shopping and Book search APIs on 2026-07-31. The subcommands
stay so an old caller gets an explanation, not SE05."""

import pytest
from typer.testing import CliRunner

from naver_cli.client import NaverClient
from naver_cli.commands.discontinued import ENDED_ON, NOTICE_URL
from naver_cli.main import app

runner = CliRunner()


@pytest.mark.parametrize("category", ["shopping", "book"])
class TestDiscontinuedSearch:
    def test_search_explains_and_fails(self, category: str) -> None:
        result = runner.invoke(app, [category, "search", "노트북"])

        assert result.exit_code == 1
        assert ENDED_ON in result.output
        assert "종료" in result.output
        assert NOTICE_URL in result.output

    def test_old_options_do_not_turn_into_a_usage_error(self, category: str) -> None:
        result = runner.invoke(
            app,
            [category, "search", "노트북", "--display", "5", "--sort", "asc", "--format", "json"],
        )

        assert result.exit_code == 1
        assert ENDED_ON in result.output
        assert "Usage" not in result.output

    def test_help_says_the_api_ended(self, category: str) -> None:
        result = runner.invoke(app, [category, "--help"])

        assert result.exit_code == 0
        assert ENDED_ON in result.output


def test_client_no_longer_exposes_the_dead_endpoints() -> None:
    assert not hasattr(NaverClient, "search_shopping")
    assert not hasattr(NaverClient, "search_book")
