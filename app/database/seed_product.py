from app.database.session import engine, get_db
from app.models.product import Product
from app.core.base import Base

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

def seed_products():
    db = next(get_db())
    for name, id in product_map.items():
        existing = db.query(Product).filter_by(id=id).first()
        if not existing:
            db.add(Product(id=id, name=name))
    db.commit()
    print("✅ Product 테이블 초기화 완료")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_products()