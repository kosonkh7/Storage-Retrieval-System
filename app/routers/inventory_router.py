from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.inventory import Inventory
from app.schemas.inventory_schema import InventoryResponse

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

# 전체 재고 목록을 반환
@router.get("/", response_model=list[InventoryResponse])
def get_all_inventory(db: Session = Depends(get_db)):
    inventory = db.query(Inventory).all()
    return inventory

# 특정 창고의 재고만 반환
@router.get("/{warehouse_id}", response_model=list[InventoryResponse])
def get_inventory_by_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.warehouse_id == warehouse_id).all()
    if not inventory:
        raise HTTPException(status_code=404, detail="재고 정보가 없습니다.")
    return inventory

# 특정 창고의 특정 품목 재고만 반환
@router.get("/{warehouse_id}/{product_id}", response_model=InventoryResponse)
def get_inventory_by_warehouse_and_product(
    warehouse_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id,
        Inventory.product_id == product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="재고 정보가 없습니다.")
    return inventory