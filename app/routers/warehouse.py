# Warehouse 관련 API 라우터

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # DB 세션 의존성 주입
from typing import List # 여러 개의 응답 처리

# DB 세션 설정 파일 불러오기
# SQLAlchemy 모델 & Pydantic 스키마 불러오기
from app.database.session import SessionLocal
from app.database.session import get_db
from app import models
from app.schemas import warehouse as warehouse_schema


router = APIRouter(
    prefix="/warehouse",
    tags=["Warehouse"],
)

# POST /warehouse/ - 새 물류센터 등록
"""
요청 JSON → SQLAlchemy 모델 변환

저장하고 commit

다시 읽어 최신 상태 반환
"""
@router.post("/", response_model=warehouse_schema.WarehouseResponse)
def create_warehouse(warehouse: warehouse_schema.WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = models.warehouse.Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

# GET /warehouse/ - 전체 물류센터 조회
"""
여러 개의 Warehouse 응답

페이지네이션 기본값: skip=0, limit=100
"""
@router.get("/", response_model=List[warehouse_schema.WarehouseResponse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    warehouses = db.query(models.warehouse.Warehouse).offset(skip).limit(limit).all()
    return warehouses