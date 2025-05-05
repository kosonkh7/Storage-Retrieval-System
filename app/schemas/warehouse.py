# Warehouse 요청 및 응답 스키마 정의

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 요청 스키마 (POST 요청 시 사용), 클라이언트가 보내는 요청 바디 스키마
class WarehouseCreate(BaseModel):
    name: str
    address: Optional[str] = None
    district_name: Optional[str] = None
    neighborhood_name: Optional[str] = None
    district_code: Optional[int] = None
    neighborhood_code: Optional[int] = None

# 응답 스키마 (조회 시 사용), 서버가 응답할 때 사용하는 스키마
class WarehouseResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    district_name: Optional[str]
    neighborhood_name: Optional[str]
    district_code: Optional[int]
    neighborhood_code: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 모델을 그대로 읽어올 수 있게 함, SQLAlchemy 모델 객체를 바로 Pydantic으로 직렬화 가능하게 해줌