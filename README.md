# naver-cli

네이버 오픈 API를 터미널에서 사용할 수 있는 CLI 도구.

## 기술 스택

- Python 3.12+
- Typer (CLI 프레임워크)
- httpx (HTTP 클라이언트)
- Pydantic (데이터 모델)
- Rich (터미널 출력)
- uv (패키지 관리)
- ruff (린터/포매터)

## 설치

```bash
uv sync
```

## 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 API 키를 설정한다.

```bash
cp .env.example .env
```

```
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here
```

네이버 개발자 센터(https://developers.naver.com)에서 애플리케이션을 등록하고 Client ID/Secret을 발급받는다.

## 사용법

### 지역 검색

```bash
# 기본 검색
uv run naver local search "강남역 맛집"

# 옵션 지정
uv run naver local search "판교 카페" --display 3 --sort comment

# 출력 형식 지정
uv run naver local search "강남역 맛집" --format text      # rich 테이블 (기본값)
uv run naver local search "강남역 맛집" --format markdown   # 마크다운 테이블
uv run naver local search "강남역 맛집" --format json       # JSON

# 도움말
uv run naver --help
uv run naver local search --help
```

### 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--display` | 검색 결과 출력 건수 (1~5) | 5 |
| `--start` | 검색 시작 위치 | 1 |
| `--sort` | 정렬 (`random`: 정확도순, `comment`: 리뷰순) | random |
| `--format` | 출력 형식 (`text`, `markdown`, `json`) | text |

## 프로젝트 구조

```
naver-cli/
├── pyproject.toml
├── .env.example
├── src/
│   └── naver_cli/
│       ├── main.py           # Typer 앱 엔트리포인트
│       ├── client.py         # 네이버 API HTTP 클라이언트
│       ├── config.py         # 설정 관리 (API 키 로딩)
│       ├── models.py         # 응답 데이터 모델 (Pydantic)
│       └── commands/
│           └── local.py      # 지역 검색 커맨드
└── tests/
    ├── conftest.py
    ├── test_client.py
    ├── test_models.py
    └── test_commands/
        └── test_local.py
```

## 개발

```bash
# 테스트
uv run pytest -v

# 린트
uv run ruff check src/ tests/

# 포맷
uv run ruff format src/ tests/
```

## 라이선스

Private
