from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum as SQLEnum, JSON
from datetime import datetime
import enum

from app.db.base import Base


class FlowerPurpose(str, enum.Enum):
    """花卉用途枚举"""
    ORNAMENTAL = "ornamental"  # 观赏
    SALE = "sale"              # 售卖
    ESSENTIAL_OIL = "essential_oil"  # 精油
    MEDICINAL = "medicinal"    # 药用
    OTHER = "other"            # 其他


class BloomSeason(str, enum.Enum):
    """开花季节枚举"""
    SPRING = "spring"          # 春季
    SUMMER = "summer"          # 夏季
    AUTUMN = "autumn"          # 秋季
    WINTER = "winter"          # 冬季
    ALL_YEAR = "all_year"      # 全年
    MULTIPLE = "multiple"      # 多季


class Flower(Base):
    """花卉模型"""
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="花卉名称")
    variety = Column(String(100), nullable=False, comment="品种")
    quantity = Column(Integer, nullable=False, default=0, comment="数量")
    plant_date = Column(Date, nullable=False, comment="种植日期")
    bloom_season = Column(SQLEnum(BloomSeason), comment="开花季节")
    bloom_seasons = Column(JSON, comment="多季开花（JSON数组）")
    colors = Column(JSON, comment="颜色列表（JSON数组）")
    purpose = Column(SQLEnum(FlowerPurpose), comment="主要用途")
    estimated_yield = Column(Float, comment="预估产量")
    yield_unit = Column(String(20), comment="产量单位（支/千克等）")
    notes = Column(String(500), comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    def __repr__(self):
        return f"<Flower {self.name} ({self.variety}) - {self.quantity}>"
