# FastAPI 메인 앱 - 전체 라우터 포함

from fastapi import FastAPI
from app.routers import warehouse


# FastAPI 앱 인스턴스 생성
# 타이틀, 설명, 버전까지 메타데이터 지정 (Docs에 자동 반영됨)
app = FastAPI(
    title="Inventory Management API",
    description="🚚 실시간 입출고 재고 관리 시스템",
    version="1.0.0",
)

# /warehouse 라우터를 메인 앱에 등록
# POST, GET API가 메인 앱에서 바로 작동
app.include_router(warehouse.router)

# 루트 경로 기본 응답
@app.get("/")
def root():
    return {"message": "Welcome to the Inventory Management API!"}


# 테스트 코드 : uvicorn app.main:app --reload