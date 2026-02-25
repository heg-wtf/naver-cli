import typer

from naver_cli.commands import blog, book, cafe, local, news, shopping

app = typer.Typer(help="네이버 오픈 API CLI 도구")
app.add_typer(local.app, name="local")
app.add_typer(book.app, name="book")
app.add_typer(blog.app, name="blog")
app.add_typer(cafe.app, name="cafe")
app.add_typer(news.app, name="news")
app.add_typer(shopping.app, name="shopping")

if __name__ == "__main__":
    app()
