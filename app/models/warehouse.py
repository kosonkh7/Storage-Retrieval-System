# 물류센터 정보를 저장하는 Warehouse 테이블 정의

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

# SQLAlchemy의 Base 클래스 생성 (모든 테이블의 부모 클래스)
Base = declarative_base()
"""
SQLAlchemy의 모든 모델은 이 Base를 상속받아 정의해.

이걸 상속한 클래스는 자동으로 테이블로 매핑돼.
"""

class Warehouse(Base):
    __tablename__ = "warehouse"  # 실제 DB에 생성될 테이블 이름
    """
    테이블 이름을 warehouse로 지정
    실제로는 CREATE TABLE warehouse (...)로 생성돼.
    """

    id = Column(Integer, primary_key=True, index=True)  # 고유 ID, 기본 키
    name = Column(String(100), nullable=False)  # 센터 이름
    address = Column(String(200), nullable=True)  # 상세 주소
    district_name = Column(String(100), nullable=True)  # 자치구 이름
    neighborhood_name = Column(String(100), nullable=True)  # 행정동 이름
    district_code = Column(Integer, nullable=True)  # 자치구 코드
    neighborhood_code = Column(Integer, nullable=True)  # 행정동 코드
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))  # 생성 시각 (기본값: 현재 시간)
    """
    timezone=True: SQLAlchemy가 이 필드에 timezone이 있다는 걸 인식
    datetime.now(timezone.utc): 명시적으로 UTC 기준 시간으로 생성
    lambda: 테이블 객체가 생성될 때마다 "지연 평가(lazy evaluation)"로 시간 설정됨
    """