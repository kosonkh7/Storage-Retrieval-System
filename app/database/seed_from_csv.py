import pandas as pd
from app.database.session import SessionLocal
from app.models import warehouse as warehouse_model
from app.models import inventory as inventory_model
from datetime import datetime, timezone

# 1️⃣ DB 세션 열기
db = SessionLocal()

# 2️⃣ warehouse.csv 읽기 & 삽입
warehouse_df = pd.read_csv('app/database/seed_data/warehouse.csv', encoding="euc-kr")

for _, row in warehouse_df.iterrows():
    wh = warehouse_model.Warehouse(
        id=int(row['id']),
        name=row['name'],
        address=row['address'],
        district_name=row['district_name'],
        neighborhood_name=row['neighborhood_name'],
        district_code=int(row['district_code']),
        neighborhood_code=int(row['neighborhood_code']),
        created_at=pd.to_datetime(row['created_at'])
    )
    db.merge(wh)  # id 고정으로 merge() 사용 → 이미 있으면 업데이트, 없으면 삽입

# 삽입만 안하고 커밋을 안하면 logistics 에서 데이터 참조가 안됨
db.commit()
print(f"✅ {len(warehouse_df)}개의 warehouse 데이터 삽입 완료.")

# 3️⃣ logistics.csv 읽기 (출고 데이터)
logistics_df = pd.read_csv('app/database/seed_data/logistics.csv', encoding="euc-kr")

# 2023-04-17만 추출 (초기 재고로 삼음)
logistics_df = logistics_df[logistics_df['date'] == 20230417]

# 품목군 매핑 (CSV 컬럼명 -> product_id)
product_map = {
    'furniture': 1,
    'other': 2,
    'book': 3,
    'digital': 4,
    'life': 5,
    'sports': 6,
    'food': 7,
    'baby': 8,
    'fashion': 9,
    'goods': 10,
    'cosmetic': 11,
}

# 각 row = 물류센터 1개
for _, row in logistics_df.iterrows():
    center_name = row['center_name']
    # warehouse_id 찾기
    warehouse_obj = db.query(warehouse_model.Warehouse).filter_by(name=center_name).first()
    if not warehouse_obj:
        print(f"❌ warehouse {center_name} 없음, 건너뜀.")
        continue

    warehouse_id = warehouse_obj.id

    # 각 품목군별로 inventory 생성
    for category_name, product_id in product_map.items():
        quantity = row[category_name] * 3  # 출고량 x 3 → 초기 재고

        inv = inventory_model.Inventory(
            warehouse_id=warehouse_id,
            product_id=product_id,
            quantity=quantity,
            updated_at=datetime.now(timezone.utc)
        )
        db.add(inv)

print(f"✅ 초기 재고 데이터 삽입 완료.")

# 커밋 & 종료
db.commit()
db.close()
print("🎉 모든 초기화 완료.")
