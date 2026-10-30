"""Stubs for Naver search APIs that no longer exist upstream.

Naver shut down the Shopping, Book and Academic (전문자료) search APIs on
2026-07-31 and moved nothing equivalent to NAVER API HUB
(https://developers.naver.com/notice/article/32564). ``shop.json`` and
``book.json`` now answer ``SE05 Invalid search api`` for every key. The old
subcommand names stay registered so a script or prompt written before the
shutdown gets a plain explanation and a non-zero exit instead of an opaque
SE05.
"""

import typer
from rich.console import Console

NOTICE_URL = "https://developers.naver.com/notice/article/32564"
ENDED_ON = "2026-07-31"

console = Console()


def build_discontinued_app(display_name: str, alternative: str) -> typer.Typer:
    """Build a Typer app whose ``search`` only explains that the API is gone.

    Args:
        display_name: 사용자에게 보여줄 검색 종류 이름 (예: "쇼핑")
        alternative: 대신 무엇을 쓰면 되는지 한 줄 안내

    Returns:
        ``search`` 서브커맨드 하나를 가진 Typer 앱. 어떤 인자·옵션이 오든
        종료 안내를 출력하고 exit code 1로 끝난다.
    """
    app = typer.Typer(help=f"네이버 {display_name} 검색 — {ENDED_ON} 종료된 API")

    @app.command(
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    )
    def search(context: typer.Context) -> None:
        """종료된 API. 안내만 출력하고 실패로 끝난다."""
        console.print(
            f"[red]네이버 {display_name} 검색 API는 {ENDED_ON}에 종료되었습니다. "
            "대체 API는 제공되지 않습니다.[/red]"
        )
        console.print(f"대신: {alternative}")
        console.print(f"공지: {NOTICE_URL}")
        raise typer.Exit(code=1)

    return app
