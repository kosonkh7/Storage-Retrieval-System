# 입출고 트랜잭션 API 라우터

"""
APIRouter: FastAPI에서 하나의 기능 묶음을 만들 때 사용하는 라우터
Depends: FastAPI가 **의존성 주입(Dependency Injection)**을 해주는 도구 (여기선 DB 세션)
HTTPException: 에러 발생 시 HTTP 응답 코드 & 메세지를 리턴
Session: SQLAlchemy DB 연결 세션 타입
List: 응답이 여러 건 반환될 때 사용
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import SessionLocal # DB 세션을 만들고 반환하는 함수 (SQLAlchemy 연결)
from app.database.session import get_db
from app import models # DB 테이블 정의
from app.schemas import inventory_transaction # 요청/응답 스키마 정의 (Pydantic)


"""
prefix: /inventory/transaction로 시작하는 경로를 다 이 라우터에서 관리
tags: Swagger UI에서 이 API 그룹의 이름으로 보임
예: /inventory/transaction/ 이렇게 API 경로가 만들어짐.
"""
router = APIRouter(
    prefix="/inventory/transaction",
    tags=["InventoryTransaction"],
)


# POST: 입출고 트랜잭션 등록
"""
@router.post("/"): POST 요청 받을 엔드포인트
response_model: 이 함수의 반환 값을 자동으로 InventoryTransactionResponse로 직렬화
transaction: 클라이언트가 보낸 JSON → InventoryTransactionCreate 스키마로 자동 검증
db: DB 세션 (FastAPI가 get_db()로 주입)
"""
@router.post("/", response_model=inventory_transaction.InventoryTransactionResponse)
def create_transaction(
    transaction: inventory_transaction.InventoryTransactionCreate,
    db: Session = Depends(get_db)
):
    try: # 중간에 예외 터지면 except 문 rollback() 실행
        # 1️⃣ 대상 재고 가져오기 (락 걸기)
        stmt = select(models.inventory.Inventory).where(
            models.inventory.Inventory.id == transaction.inventory_id
        ).with_for_update() # 해당 row를 읽고 작업하는 동안 다른 트랜잭션은 접근할 수 없음.
        inventory = db.execute(stmt).scalar_one_or_none()

        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")

        # 2️⃣ 입고/출고 반영
        if transaction.transaction_type not in ["in", "out"]: # 타입 체크: 'in', 'out' 외 값이 오면 400 에러
            raise HTTPException(status_code=400, detail="Invalid transaction type")

        before_qty = inventory.quantity
        if transaction.transaction_type == "in": # 입고면 +, 출고면 - 로 계산
            after_qty = before_qty + transaction.quantity
        else:
            if transaction.quantity > before_qty: # 출고 시 → 재고보다 많으면 에러
                raise HTTPException(status_code=400, detail="출고 수량이 재고보다 많습니다.") # 이 부분에서 에러 발생 가능성
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
        inventory.quantity = after_qty # 재고 테이블의 quantity도 최신 값으로 업데이트

        # 5️⃣ 커밋
        """
        commit(): 트랜잭션을 DB에 영구 반영
        refresh(): 새로 만든 트랜잭션 객체의 최신 상태 다시 가져오기
        """
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

# GET: 전체 트랜잭션 조회
@router.get("/", response_model=List[inventory_transaction.InventoryTransactionResponse])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.inventory_transaction.InventoryTransaction).offset(skip).limit(limit).all()
    return transactions # 결과는 트랜잭션 리스트 반환

"""
DB 세션 의존성:	FastAPI에서 가장 안정적인 DB 연결 방식
트랜잭션 타입 구분:	비즈니스 로직이 명확하게 분리
출고 초과 검증:	데이터 무결성 확보
트랜잭션 기록 + 실시간 재고:	재고 꼬임 문제 방지 & 감사 추적 가능
orm_mode:	SQLAlchemy → Pydantic 변환 쉽게 처리
"""

# GET: 특정 재고(inventory_id)에 대한 이력만 조회
@router.get("/{inventory_id}", response_model=List[inventory_transaction.InventoryTransactionResponse])
def read_transactions_by_inventory(
    inventory_id: int,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):  
    # 쿼리 시작: 특정 inventory_id의 이력만 조회
    query = db.query(models.inventory_transaction.InventoryTransaction).filter(
        models.inventory_transaction.InventoryTransaction.inventory_id == inventory_id
    )
    # 트랜잭션 타입이 지정되면 필터 추가 ('in' 또는 'out')
    if transaction_type:
        if transaction_type not in ["in", "out"]:
            raise HTTPException(status_code=400, detail="Invalid transaction type")
        query = query.filter(models.inventory_transaction.InventoryTransaction.transaction_type == transaction_type)

    # 최종 결과 가져오기
    transactions = query.all()

    if not transactions:
        raise HTTPException(status_code=404, detail="입출고 이력이 없습니다.")
    
    # 결과 반환 (FastAPI가 자동으로 스키마에 맞춰 Pydantic 스키마로 직렬화)
    return transactions