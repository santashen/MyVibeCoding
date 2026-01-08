from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class YieldRecord(Base):
    """产量记录模型 - 记录每次收获的产量"""
    __tablename__ = "yield_records"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, comment="关联粮食ID")
    record_date = Column(Date, nullable=False, comment="记录日期")
    quantity = Column(Float, nullable=False, comment="产量数量")
    unit = Column(String(20), comment="单位")
    area_harvested = Column(Float, comment="收获面积（亩）")
    notes = Column(String(500), comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关联
    crop = relationship("Crop", back_populates="yield_records")

    def __repr__(self):
        return f"<YieldRecord {self.crop_id} - {self.quantity}{self.unit} on {self.record_date}>"
