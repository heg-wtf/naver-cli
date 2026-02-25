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

### pip

```bash
pip install .
```

설치 후 `naver-cli` 명령으로 실행할 수 있다.

```bash
naver-cli --help
```

### uv (개발용)

```bash
uv sync
uv run naver-cli --help
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
naver-cli local search "강남역 맛집"
naver-cli local search "판교 카페" --display 3 --sort comment
```

### 책 검색

```bash
naver-cli book search "파이썬"
naver-cli book search "파이썬" --display 20 --sort date
```

### 블로그 검색

```bash
naver-cli blog search "맛집 추천"
naver-cli blog search "맛집 추천" --sort date
```

### 카페글 검색

```bash
naver-cli cafe search "여행 후기"
naver-cli cafe search "여행 후기" --display 15
```

### 뉴스 검색

```bash
naver-cli news search "경제"
naver-cli news search "경제" --sort date --display 20
```

### 쇼핑 검색

```bash
naver-cli shopping search "노트북"
naver-cli shopping search "노트북" --sort asc  # 가격 낮은순
```

### 출력 형식

모든 검색 커맨드에서 `--format` 옵션으로 출력 형식을 지정할 수 있다.

```bash
naver-cli local search "강남역 맛집" --format text      # rich 테이블 (기본값)
naver-cli local search "강남역 맛집" --format markdown   # 마크다운 테이블
naver-cli local search "강남역 맛집" --format json       # JSON
```

### 공통 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--display` | 검색 결과 출력 건수 | 검색 타입별 상이 |
| `--start` | 검색 시작 위치 | 1 |
| `--sort` | 정렬 옵션 | 검색 타입별 상이 |
| `--format` | 출력 형식 (`text`, `markdown`, `json`) | text |

### 검색 타입별 정렬 옵션

| 타입 | 정렬 옵션 |
|------|-----------|
| local | `random` (정확도순), `comment` (리뷰순) |
| book | `sim` (정확도순), `date` (출간일순), `count` (판매량순) |
| blog | `sim` (정확도순), `date` (날짜순) |
| cafe | `sim` (정확도순), `date` (날짜순) |
| news | `sim` (정확도순), `date` (날짜순) |
| shopping | `sim` (정확도순), `date` (날짜순), `asc` (가격낮은순), `dsc` (가격높은순) |

## 프로젝트 구조

```
naver-cli/
├── pyproject.toml
├── .env.example
├── src/
│   └── naver_cli/
│       ├── main.py           # Typer 앱 엔트리포인트 (ASCII 배너)
│       ├── client.py         # 네이버 API HTTP 클라이언트
│       ├── config.py         # 설정 관리 (API 키 로딩)
│       ├── models.py         # 응답 데이터 모델 (Pydantic)
│       └── commands/
│           ├── __init__.py   # OutputFormat 공통 모듈
│           ├── local.py      # 지역 검색 커맨드
│           ├── book.py       # 책 검색 커맨드
│           ├── blog.py       # 블로그 검색 커맨드
│           ├── cafe.py       # 카페글 검색 커맨드
│           ├── news.py       # 뉴스 검색 커맨드
│           └── shopping.py   # 쇼핑 검색 커맨드
└── tests/
    ├── conftest.py
    ├── test_client.py
    ├── test_models.py
    └── test_commands/
        ├── test_local.py
        ├── test_book.py
        ├── test_blog.py
        ├── test_cafe.py
        ├── test_news.py
        └── test_shopping.py
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
