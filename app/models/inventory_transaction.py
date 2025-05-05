# 입출고 기록을 저장하는 InventoryTransaction 테이블 정의

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.base import Base
from datetime import datetime, timezone

class InventoryTransaction(Base):
    __tablename__ = "inventory_transaction"

    """
    transaction_type	'in' 또는 'out' (입고/출고 구분)
    quantity	입출고 수량
    before_quantity / after_quantity	트랜잭션 발생 전/후 재고 수량 기록
    memo	비고, 입출고 사유 등
    created_at	발생 시각 (UTC, timezone-aware)
    """

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    transaction_type = Column(String(10), nullable=False)  # 'in' 또는 'out' (입고/출고 구분)
    quantity = Column(Integer, nullable=False)
    before_quantity = Column(Integer, nullable=False)
    after_quantity = Column(Integer, nullable=False)
    memo = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    inventory = relationship("Inventory", backref="transactions")