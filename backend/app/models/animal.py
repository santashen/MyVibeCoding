from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum as SQLEnum
from datetime import datetime
import enum

from app.db.base import Base


class ProductType(str, enum.Enum):
    """产品类型枚举"""
    MILK = "milk"              # 奶
    EGG = "egg"                # 蛋
    WOOL = "wool"              # 毛
    MEAT = "meat"              # 肉
    HONEY = "honey"            # 蜂蜜
    OTHER = "other"            # 其他


class Animal(Base):
    """动物模型"""
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="动物名称")
    variety = Column(String(100), nullable=False, comment="品种")
    quantity = Column(Integer, nullable=False, default=0, comment="数量")
    acquire_date = Column(Date, nullable=False, comment="购入/出生日期")
    product_type = Column(SQLEnum(ProductType), comment="产产品类型")
    estimated_daily_yield = Column(Float, comment="预估日产产量")
    yield_unit = Column(String(20), comment="产量单位（升/千克/个等）")
    notes = Column(String(500), comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    def __repr__(self):
        return f"<Animal {self.name} ({self.variety}) - {self.quantity}>"
