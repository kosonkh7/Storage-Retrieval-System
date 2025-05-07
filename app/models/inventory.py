# 재고 정보를 저장하는 Inventory 테이블 정의

# SQLAlchemy ORM 기본 도구 + 관계 설정
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.core.base import Base  # core에서 Base 가져오기
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Inventory(Base):
    __tablename__ = "inventory"  # 테이블 이름

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)  # 물류센터 ID (FK)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)  # 품목군 ID (심플하게 숫자로 처리)
    quantity = Column(Integer, default=0)  # 현재 재고 수량 (처음엔 무조건 0으로 시작)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # 관계 설정 (선택적)
    # SQLAlchemy 관계 설정 (나중에 Warehouse 객체에서 inventories로 연결 가능)
    warehouse = relationship("Warehouse", backref="inventories")
    product = relationship("Product", backref="inventories")