import typer
from rich.console import Console

from naver_cli.commands import blog, book, cafe, local, news, shopping

BANNER = r"""
 _   _    _    __     __ _____ ____       ____  _     ___
| \ | |  / \   \ \   / /| ____|  _ \     / ___|| |   |_ _|
|  \| | / _ \   \ \ / / |  _| | |_) |   | |   | |    | |
| |\  |/ ___ \   \ V /  | |___|  _ <    | |___| |___ | |
|_| \_/_/   \_\   \_/   |_____|_| \_\    \____|_____|___|
"""

console = Console()
app = typer.Typer(help="네이버 오픈 API CLI 도구", invoke_without_command=True)


@app.callback()
def main(context: typer.Context) -> None:
    """네이버 오픈 API CLI 도구."""
    if context.invoked_subcommand is None:
        console.print(BANNER, style="bold green")
        console.print("  네이버 오픈 API CLI 도구\n", style="bold")
        console.print("  사용법: [cyan]naver --help[/cyan] 로 도움말을 확인하세요.\n")


app.add_typer(local.app, name="local")
app.add_typer(book.app, name="book")
app.add_typer(blog.app, name="blog")
app.add_typer(cafe.app, name="cafe")
app.add_typer(news.app, name="news")
app.add_typer(shopping.app, name="shopping")

if __name__ == "__main__":
    app()
