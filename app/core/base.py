from sqlalchemy.orm import declarative_base

# 모든 모델이 이 Base를 상속해서 같은 메타데이터를 공유
Base = declarative_base()