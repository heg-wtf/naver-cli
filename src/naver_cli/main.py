import typer
from rich.console import Console

from naver_cli import __version__
from naver_cli.commands import blog, book, cafe, local, news, shopping

BANNER = r"""
 ███╗   ██╗ █████╗ ██╗   ██╗███████╗██████╗      ██████╗██╗     ██╗
 ████╗  ██║██╔══██╗██║   ██║██╔════╝██╔══██╗    ██╔════╝██║     ██║
 ██╔██╗ ██║███████║██║   ██║█████╗  ██████╔╝    ██║     ██║     ██║
 ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██║     ██║     ██║
 ██║ ╚████║██║  ██║ ╚████╔╝ ███████╗██║  ██║    ╚██████╗███████╗██║
 ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝     ╚═════╝╚══════╝╚═╝
"""

console = Console()
app = typer.Typer(help="네이버 오픈 API CLI 도구", invoke_without_command=True)


def _print_version(value: bool) -> None:
    """Plain `name version` on stdout — HEG-406 needs it machine-readable so
    the monthly dependency audit can diff installed CLIs against upstream."""
    if value:
        print(f"naver-cli {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    context: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        callback=_print_version,
        is_eager=True,
        help="버전을 출력하고 종료합니다.",
    ),
) -> None:
    """네이버 오픈 API CLI 도구."""
    if context.invoked_subcommand is None:
        console.print(f"[#2DB400]{BANNER}[/#2DB400]")
        console.print(f"  [dim]v{__version__}[/dim]\n")
        console.print("  사용법: [cyan]naver --help[/cyan] 로 도움말을 확인하세요.\n")


app.add_typer(local.app, name="local")
app.add_typer(book.app, name="book")
app.add_typer(blog.app, name="blog")
app.add_typer(cafe.app, name="cafe")
app.add_typer(news.app, name="news")
app.add_typer(shopping.app, name="shopping")

if __name__ == "__main__":
    app()
