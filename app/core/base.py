from sqlalchemy.orm import declarative_base

# 모든 모델이 이 Base를 상속해서 같은 메타데이터를 공유
Base = declarative_base()

"""
core/base.py로 모델의 메타데이터 통합 -> 외래키 참조 이슈 해결
"""