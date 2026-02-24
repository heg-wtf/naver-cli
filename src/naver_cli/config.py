import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")

NAVER_CLIENT_ID: str = os.environ.get("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET: str = os.environ.get("NAVER_CLIENT_SECRET", "")


def validate_credentials() -> bool:
    """API 자격 증명이 설정되어 있는지 확인한다."""
    return bool(NAVER_CLIENT_ID and NAVER_CLIENT_SECRET)
