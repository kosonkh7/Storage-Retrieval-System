from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.inventory import Inventory
from app.schemas.inventory_schema import InventoryOut

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("/", response_model=list[InventoryOut])
def get_all_inventory(db: Session = Depends(get_db)):
    inventory = db.query(Inventory).all()
    return inventory

@router.get("/{warehouse_id}", response_model=list[InventoryOut])
def get_inventory_by_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.warehouse_id == warehouse_id).all()
    if not inventory:
        raise HTTPException(status_code=404, detail="재고 정보가 없습니다.")
    return inventory