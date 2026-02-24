import typer

from naver_cli.commands import local

app = typer.Typer(help="네이버 오픈 API CLI 도구")
app.add_typer(local.app, name="local")

if __name__ == "__main__":
    app()
