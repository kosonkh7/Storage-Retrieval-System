from pydantic import BaseModel
from datetime import datetime

class InventoryResponse(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    updated_at: datetime

    class Config:
        orm_mode = True