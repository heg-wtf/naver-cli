# naver-cli

네이버 오픈 API CLI 도구. 6종 검색 API를 지원한다 (지역, 책, 블로그, 카페, 뉴스, 쇼핑).

## 주요 명령어

```bash
uv sync              # 의존성 설치
uv run pytest -v     # 테스트 실행
uv run ruff check src/ tests/   # 린트
uv run ruff format src/ tests/  # 포맷
uv run naver --help             # CLI 도움말
```

## 프로젝트 구조

- `src/naver_cli/main.py` - Typer 앱 엔트리포인트, ASCII 배너, 서브커맨드 등록
- `src/naver_cli/client.py` - NaverClient (httpx 기반 API 클라이언트, 6종 검색)
- `src/naver_cli/config.py` - .env에서 API 키 로딩
- `src/naver_cli/models.py` - Pydantic 응답 모델 (6종 검색별 Item/Response)
- `src/naver_cli/commands/` - 검색 커맨드 모듈 (local, book, blog, cafe, news, shopping)
- `src/naver_cli/commands/__init__.py` - OutputFormat 공통 enum
- `tests/` - pytest 테스트 (pytest-httpx로 HTTP mock)

## 코드 스타일

- Python 3.12+, ruff (line-length 99)
- 타입 힌트 필수, `list[str]` / `X | None` 형태
- Google-style docstring
- 약어 사용 지양 (full text 사용)

## 설정

- 환경 변수: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` (.env 파일)
- CLI 엔트리포인트: `naver`, `naver-cli` (pyproject.toml `[project.scripts]`)

## API 참조

- 베이스 URL: `https://openapi.naver.com/v1/search`
- 인증 헤더: `X-Naver-Client-Id`, `X-Naver-Client-Secret`
- 엔드포인트: `local.json`, `book.json`, `blog.json`, `cafearticle.json`, `news.json`, `shop.json`
