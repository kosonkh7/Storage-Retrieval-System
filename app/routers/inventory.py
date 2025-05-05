# 입출고 트랜잭션 API 라우터

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import SessionLocal
from app import models
from app.schemas import inventory as inventory_schema

router = APIRouter(
    prefix="/inventory/transaction",
    tags=["InventoryTransaction"],
)

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: 입출고 트랜잭션 등록
@router.post("/", response_model=inventory_schema.InventoryTransactionResponse)
def create_transaction(
    transaction: inventory_schema.InventoryTransactionCreate,
    db: Session = Depends(get_db)
):
    # 1️⃣ 대상 재고 가져오기
    inventory = db.query(models.inventory.Inventory).filter(
        models.inventory.Inventory.id == transaction.inventory_id
    ).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    # 2️⃣ 입고/출고 반영
    if transaction.transaction_type not in ["in", "out"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    before_qty = inventory.quantity
    if transaction.transaction_type == "in":
        after_qty = before_qty + transaction.quantity
    else:
        if transaction.quantity > before_qty:
            raise HTTPException(status_code=400, detail="출고 수량이 재고보다 많습니다.")
        after_qty = before_qty - transaction.quantity

    # 3️⃣ 트랜잭션 기록 저장
    db_transaction = models.inventory_transaction.InventoryTransaction(
        inventory_id=transaction.inventory_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        before_quantity=before_qty,
        after_quantity=after_qty,
        memo=transaction.memo,
    )
    db.add(db_transaction)

    # 4️⃣ 재고 업데이트
    inventory.quantity = after_qty
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# GET: 전체 트랜잭션 조회
@router.get("/", response_model=List[inventory_schema.InventoryTransactionResponse])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.inventory_transaction.InventoryTransaction).offset(skip).limit(limit).all()
    return transactions