# naver-cli

네이버 오픈 API CLI 도구. 4종 검색 API를 지원한다 (지역, 블로그, 카페, 뉴스).
책·쇼핑 검색은 네이버가 2026-07-31에 종료했다 (대체 API 없음,
https://developers.naver.com/notice/article/32564) — `book`/`shopping` 서브커맨드는
종료 안내만 출력하고 exit 1로 끝나는 스텁이다 (`commands/discontinued.py`).

## 주요 명령어

```bash
uv sync              # 의존성 설치
make test            # 테스트 실행
make lint            # 포맷 + 린트 (ruff)
uv run naver --help             # CLI 도움말
```

## 프로젝트 구조

- `src/naver_cli/main.py` - Typer 앱 엔트리포인트, ASCII 배너, 서브커맨드 등록
- `src/naver_cli/client.py` - NaverClient (httpx 기반 API 클라이언트, 4종 검색)
- `src/naver_cli/config.py` - .env에서 API 키 로딩
- `src/naver_cli/models.py` - Pydantic 응답 모델 (4종 검색별 Item/Response)
- `src/naver_cli/commands/` - 검색 커맨드 모듈 (local, blog, cafe, news) + 종료 스텁 (book, shopping)
- `src/naver_cli/commands/__init__.py` - OutputFormat 공통 enum
- `tests/` - pytest 테스트 (pytest-httpx로 HTTP mock)

## 코드 스타일

- Python 3.12+, ruff (line-length 99)
- 타입 힌트 필수, `list[str]` / `X | None` 형태
- Google-style docstring
- 약어 사용 지양 (full text 사용)

## 설정

- 환경 변수: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`
  - 셸 환경변수 직접 설정 또는 현재 작업 디렉토리의 `.env` 파일에서 로딩
- CLI 엔트리포인트: `naver`, `naver-cli` (pyproject.toml `[project.scripts]`)

## API 참조

- 베이스 URL: `https://openapi.naver.com/v1/search`
- 인증 헤더: `X-Naver-Client-Id`, `X-Naver-Client-Secret`
- 엔드포인트: `local.json`, `blog.json`, `cafearticle.json`, `news.json`
- `book.json`, `shop.json`은 2026-07-31부로 모든 키에 `SE05 Invalid search api`를 돌려준다
