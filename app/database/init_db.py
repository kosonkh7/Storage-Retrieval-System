# DB 테이블을 실제로 생성하는 초기화 스크립트

from sqlalchemy.orm import declarative_base
from app.database.session import engine
from app.models.warehouse import Base as WarehouseBase  # models/__init__.py 덕분에 여기서 한 번에 인식됨
from app.models.inventory import Base as InventoryBase

# Base를 직접 임포트하지 않고도, 모델이 모두 등록되어 있으면 create_all 가능
from app.models.warehouse import Base

def init_db():
    print("📦 Creating all tables in the database...")
    WarehouseBase.metadata.create_all(bind=engine)
    InventoryBase.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

# 직접 실행할 수 있게 설정
if __name__ == "__main__":
    init_db()