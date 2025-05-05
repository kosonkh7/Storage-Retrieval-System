# DB 테이블을 실제로 생성하는 초기화 스크립트

from sqlalchemy.orm import declarative_base
from app.database.session import engine
from app.core.base import Base  # 이제 모든 모델이 같은 Base를 공유
from app import models  # 모델들을 등록해서 Base에 메타데이터로 추가

def init_db():
    print("📦 Creating all tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

# 직접 실행할 수 있게 설정
if __name__ == "__main__":
    init_db()