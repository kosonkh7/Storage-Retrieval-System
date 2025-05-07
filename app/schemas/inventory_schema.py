from pydantic import BaseModel
from datetime import datetime

class ProductInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class InventoryResponse(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    updated_at: datetime
    product: ProductInfo

    class Config:
        orm_mode = True