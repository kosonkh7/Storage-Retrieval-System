from pydantic import BaseModel
from datetime import datetime

class InventoryOut(BaseModel):
    id: int
    warehouse_id: int
    category_name: str
    stock: float
    created_at: datetime

    class Config:
        orm_mode = True