# 베이스 이미지
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치용 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 전체 코드 복사
COPY . .

# 포트 노출
EXPOSE 8002

# 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload", "--log-level", "info"]
