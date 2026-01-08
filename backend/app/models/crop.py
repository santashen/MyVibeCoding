from sqlalchemy import Column, Integer, String, Float, Date, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class CropStatus(str, enum.Enum):
    """粮食状态枚举"""
    GROWING = "growing"      # 生长中
    HARVESTED = "harvested"  # 已收获
    FAILED = "failed"        # 失败/废弃


class CropUnit(str, enum.Enum):
    """产量单位枚举"""
    TON = "ton"              # 吨
    KG = "kg"                # 千克
    GRAM = "gram"            # 克


class Crop(Base):
    """粮食模型"""
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="粮食名称")
    variety = Column(String(100), nullable=False, comment="品种")
    area = Column(Float, nullable=False, comment="种植面积（亩）")
    plant_date = Column(Date, nullable=False, comment="种植日期")
    expected_harvest_date = Column(Date, comment="预计收获日期")
    actual_harvest_date = Column(Date, comment="实际收获日期")
    total_yield = Column(Float, default=0.0, comment="实际总产量")
    unit = Column(SQLEnum(CropUnit), default=CropUnit.KG, comment="产量单位")
    status = Column(SQLEnum(CropStatus), default=CropStatus.GROWING, comment="状态")
    notes = Column(String(500), comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联产量记录
    yield_records = relationship(
        "YieldRecord",
        back_populates="crop",
        cascade="all, delete-orphan",
        order_by="YieldRecord.record_date.desc()"
    )

    def __repr__(self):
        return f"<Crop {self.name} ({self.variety}) - {self.status}>"
