# config.py
import os
from dotenv import load_dotenv
import validators

# .env 파일의 환경 변수 로드
load_dotenv()

# BASE_URL - suno server용
BASE_URL = os.getenv("BASE_URL")

# BASE_URL이 유효한 URL인지 확인하고, http:// 또는 https://로 시작하지 않으면 기본적으로 http:// 추가
if not validators.url(BASE_URL):
    raise ValueError("유효하지 않은 BASE_URL입니다. .env 파일을 확인하세요.")

# 스웨거 URL 설정 (예시로 /swagger/v1 사용)
SWAGGER_URL = f"{BASE_URL}/api/custom_generate"