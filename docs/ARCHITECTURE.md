# 아키텍처

## 개요

naver-cli는 네이버 오픈 API를 CLI로 제공하는 도구이다. 레이어드 구조로 설계되어 있다.

## 레이어 구조

```
CLI 커맨드 (commands/)
    ↓
API 클라이언트 (client.py)
    ↓
데이터 모델 (models.py)
```

### 1. CLI 레이어 (`main.py`, `commands/`)

- Typer 기반 커맨드 정의
- `main.py`: 앱 엔트리포인트, ASCII 배너 표시 (서브커맨드 없이 실행 시), 서브커맨드 등록
- `commands/`: 6종 검색 커맨드 (local, book, blog, cafe, news, shopping)
- 사용자 입력 검증 및 출력 포매팅
- 출력 형식: text (rich 테이블), markdown, json

### 2. 클라이언트 레이어 (`client.py`)

- `NaverClient` 클래스가 httpx로 API를 호출
- 인증 헤더 자동 설정
- API 에러를 `NaverApiError`로 변환

### 3. 모델 레이어 (`models.py`)

- Pydantic BaseModel 기반 응답 파싱
- HTML 태그 자동 제거 (field_validator)

### 4. 설정 (`config.py`)

- 셸 환경변수 또는 python-dotenv로 현재 작업 디렉토리의 `.env` 파일에서 API 키 로딩
- pip 설치 시에는 셸 환경변수 직접 설정 권장

## 확장 방법

새로운 검색 API 추가 시:

1. `models.py`에 응답 모델 추가
2. `client.py`의 `NaverClient`에 호출 메서드 추가
3. `commands/`에 새 커맨드 모듈 생성
4. `main.py`에 커맨드 등록 (`app.add_typer`)
