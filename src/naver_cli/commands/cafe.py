import json
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from naver_cli.client import NaverApiError, NaverClient
from naver_cli.commands import OutputFormat
from naver_cli.config import validate_credentials
from naver_cli.models import CafeSearchResponse

app = typer.Typer(help="네이버 카페글 검색")
console = Console()


def _print_as_text(query: str, result: CafeSearchResponse) -> None:
    """rich 테이블 형태로 출력한다."""
    table = Table(title=f"'{query}' 카페글 검색 결과 (총 {result.total}건)")
    table.add_column("제목", style="bold cyan", no_wrap=True)
    table.add_column("카페명", style="green")
    table.add_column("링크")

    for item in result.items:
        table.add_row(item.title, item.cafename, item.link)

    console.print(table)


def _print_as_markdown(query: str, result: CafeSearchResponse) -> None:
    """마크다운 테이블 형태로 출력한다."""
    lines = [
        f"### '{query}' 카페글 검색 결과 (총 {result.total}건)",
        "",
        "| 제목 | 카페명 | 링크 |",
        "|------|--------|------|",
    ]
    for item in result.items:
        lines.append(f"| {item.title} | {item.cafename} | {item.link} |")

    console.print("\n".join(lines))


def _print_as_json(result: CafeSearchResponse) -> None:
    """JSON 형태로 출력한다."""
    data = {
        "total": result.total,
        "start": result.start,
        "display": result.display,
        "items": [
            {
                "title": item.title,
                "link": item.link,
                "description": item.description,
                "cafename": item.cafename,
                "cafeurl": item.cafeurl,
            }
            for item in result.items
        ],
    }
    console.print(json.dumps(data, ensure_ascii=False, indent=2))


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="검색어")],
    display: Annotated[int, typer.Option(help="검색 결과 출력 건수 (1~100)")] = 10,
    start: Annotated[int, typer.Option(help="검색 시작 위치")] = 1,
    sort: Annotated[str, typer.Option(help="정렬 (sim: 정확도순, date: 날짜순)")] = "sim",
    output_format: Annotated[
        OutputFormat, typer.Option("--format", help="출력 형식 (text, markdown, json)")
    ] = OutputFormat.TEXT,
) -> None:
    """네이버 카페글 검색을 수행한다."""
    if not validate_credentials():
        console.print("[red]NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET 환경 변수를 설정해주세요.[/red]")
        raise typer.Exit(code=1)

    client = NaverClient()

    try:
        result = client.search_cafe(query=query, display=display, start=start, sort=sort)
    except NaverApiError as error:
        console.print(f"[red]API 오류: {error}[/red]")
        raise typer.Exit(code=1) from error

    if not result.items:
        console.print("[yellow]검색 결과가 없습니다.[/yellow]")
        return

    match output_format:
        case OutputFormat.TEXT:
            _print_as_text(query, result)
        case OutputFormat.MARKDOWN:
            _print_as_markdown(query, result)
        case OutputFormat.JSON:
            _print_as_json(result)
