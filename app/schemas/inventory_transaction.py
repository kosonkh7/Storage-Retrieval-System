# 입출고 요청/응답 스키마 정의

from pydantic import BaseModel # JSON 요청/응답 데이터 검증
from typing import Optional
from datetime import datetime

# 입출고 트랜잭션 요청 시 사용하는 스키마 (inventory_id, transaction_type, quantity, memo)
class InventoryTransactionCreate(BaseModel):
    inventory_id: int
    transaction_type: str  # 'in' or 'out'
    quantity: int
    memo: Optional[str] = None

# 입출고 트랜잭션 응답 시 사용하는 스키마 (DB의 전체 내용 + before_quantity, after_quantity)
class InventoryTransactionResponse(BaseModel):
    id: int
    inventory_id: int
    transaction_type: str
    quantity: int
    before_quantity: int
    after_quantity: int
    memo: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True # SQLAlchemy 모델 → 바로 직렬화 가능