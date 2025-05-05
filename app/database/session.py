# SQLAlchemy 엔진과 세션을 생성하는 파일.
# FastAPI 앱에서 SQLAlchemy를 통해 DB에 연결하고, 트랜잭션 처리할 수 있는 세션 객체.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.config import SQLALCHEMY_DATABASE_URL

# SQLAlchemy 엔진 생성
# echo=True로 설정하면 실행되는 SQL이 로그에 출력됩니다 (개발 시 유용)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,              # 개발 단계에서는 SQL 로그 출력
    pool_pre_ping=True      # 연결 풀 유지 중 연결 확인
)
"""
create_engine: DB와 연결해주는 핵심 객체

echo=True: 터미널에 SQL이 출력됨 (디버깅에 매우 유용!)
"""

# 세션 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
SessionLocal: 매 API 요청마다 생성할 DB 세션 객체

autocommit=False: 직접 commit 해야 DB 반영됨

autoflush=False: 커밋 전까지 DB에 반영 안 됨 (명시적 처리 권장)
"""