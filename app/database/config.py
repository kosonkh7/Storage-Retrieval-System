# DB 연결 정보를 정의합니다.

from dotenv import load_dotenv
import os

# .env 파일 불러오기
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy 연결 문자열 구성
# 형식: dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

"""
"mysql+pymysql://..."	SQLAlchemy에서 MySQL을 PyMySQL 드라이버로 연결하는 형식
root:1234	MySQL 사용자명과 비밀번호
127.0.0.1:3306	로컬 호스트 IP와 포트 번호
/transSys	사용할 데이터베이스 이름
"""