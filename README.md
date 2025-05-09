## 📦 FastAPI 기반 실시간 재고 입출고 관리 시스템

# 프로젝트 개요
FastAPI + SQLAlchemy + MySQL을 기반으로 실제 서비스 수준의 재고 관리 API를 설계하고, <br>
트랜잭션 제어 및 동시성 문제 대응, DB 성능 최적화까지 구현한 서비스입니다. <br>

단순한 CRUD 서비스에서 더 나아가 <br>
실제 운영 환경에서 발생할 수 있는 문제들을 설계 단계에서부터 가정하여 <br>
데이터 정합성과 성능을 확보하는 서비스 개발을 목표 했습니다. <br>

# 기술 스택

### 🔧 백엔드
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-CA5040?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/pydantic-009688?style=for-the-badge)

### 🗄️ 데이터베이스
![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### 🚀 운영/배포
![Uvicorn](https://img.shields.io/badge/uvicorn-111111?style=for-the-badge)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### 📝 문서화
![GitHub](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)
![Markdown](https://img.shields.io/badge/markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)
![ERD](https://img.shields.io/badge/ERD%20Diagram-FF6F61?style=for-the-badge)


# 프로젝트 주요 특징
✅ 트랜잭션 기반 재고 정합성 보장

입출고 처리 시 SQLAlchemy의 pessimistic lock (비관적 락)을 적용

출고량 초과, 동시 출고 충돌 등 실제 발생 가능한 문제 방어

✅ MySQL 인덱스 최적화

조회 성능을 높이기 위해 단일 및 복합 인덱스 설계

✅ MSA를 위한 HTTP API 설계

FastAPI를 사용해 독립 모듈화된 라우터/스키마/모델/DB 분리

컨테이너 환경(Docker) 배포까지 확장 가능성 고려


# 주요 설계
테이블	설명
Warehouse	물류센터 정보
Product	품목군 정보 (예: furniture, food)
Inventory	창고별 품목 재고 상태
InventoryTransaction	입출고 이력 기록

📈 인덱스 최적화
inventory(warehouse_id, product_id) → 창고 + 품목 복합 조회 최적화

inventory_transaction(inventory_id, transaction_type) → 특정 품목 입출고 내역 필터링 속도 향상

Slow Query 탐지 후 추가 인덱스 적용 → 확장 시 성능 문제 최소화

🔐 트랜잭션 & 락 처리
출고 처리 시, pessimistic lock 사용
→ 동일 재고의 동시 출고 요청 시, 데이터 충돌 방지

예외 상황 (재고 부족, 잘못된 요청) 전부 HTTP 예외 처리로 방어

# API 설계
- GET	/inventory/	전체 재고 조회 <br>
- GET	/inventory/{warehouse_id}	특정 창고 재고 조회 <br>
- POST	/inventory/transaction/	입출고 트랜잭션 처리 <br>
- GET	/inventory/transaction/	전체 입출고 내역 조회 <br>
- GET	/inventory/transaction/{inventory_id}	특정 재고 입출고 내역 조회 <br>

🌟 차별화 포인트
✅ 단순 CRUD 프로젝트를 넘어서 트랜잭션 처리와 동시성 문제까지 고려한 설계
✅ MySQL 인덱스 튜닝 및 쿼리 성능 최적화 적용
✅ 실서비스에 필요한 API 모듈화 및 확장 가능성 고려
✅ GitHub 문서화 → 누구나 읽고 따라할 수 있는 실전형 포트폴리오

🏆 학습/성장 포인트
FastAPI 기반 REST API 설계 및 배포 경험

SQLAlchemy ORM 고급 기능 (트랜잭션, 락, 최적화) 실전 적용

데이터베이스 인덱스 최적화 및 쿼리 성능 분석

MSA 기반 서비스 설계 및 모듈화 아키텍처 경험

GitHub를 통한 프로젝트 문서화 및 오픈소스화 준비

#  프로젝트 실행 방법
### 1️⃣ 의존성 설치
pip install -r requirements.txt

### 2️⃣ MySQL DB 세팅 (+ 초기 데이터 삽입)
python -m app.database.init_db
python -m app.database.seed_from_csv
python -m app.database.seed_product

### 3️⃣ FastAPI 서버 실행
uvicorn app.main:app --reload

### 4️⃣ Swagger UI에서 API 테스트
http://localhost:8000/docs

# 향후 확장 계획
- Docker로 서비스 컨테이너화
- Alembic으로 마이그레이션 관리
- FastAPI 비동기 처리로 성능 개선
- GitHub Actions로 CI/CD 자동화 구축
- Prometheus + Grafana로 모니터링 구축
