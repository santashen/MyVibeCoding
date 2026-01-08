from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class CropStatus(str, Enum):
    GROWING = "growing"
    HARVESTED = "harvested"
    FAILED = "failed"


class CropUnit(str, Enum):
    TON = "ton"
    KG = "kg"
    GRAM = "gram"


class CropBase(BaseModel):
    """粮食基础Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="粮食名称")
    variety: str = Field(..., min_length=1, max_length=100, description="品种")
    area: float = Field(..., gt=0, description="种植面积（亩）")
    plant_date: date = Field(..., description="种植日期")
    expected_harvest_date: Optional[date] = Field(None, description="预计收获日期")
    unit: CropUnit = Field(CropUnit.KG, description="产量单位")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class CropCreate(CropBase):
    """创建粮食Schema"""
    pass


class CropUpdate(BaseModel):
    """更新粮食Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    variety: Optional[str] = Field(None, min_length=1, max_length=100)
    area: Optional[float] = Field(None, gt=0)
    plant_date: Optional[date] = None
    expected_harvest_date: Optional[date] = None
    actual_harvest_date: Optional[date] = None
    total_yield: Optional[float] = Field(None, ge=0)
    unit: Optional[CropUnit] = None
    status: Optional[CropStatus] = None
    notes: Optional[str] = Field(None, max_length=500)


class CropHarvestUpdate(BaseModel):
    """收获Schema"""
    actual_harvest_date: date = Field(..., description="实际收获日期")
    yield_quantity: float = Field(..., gt=0, description="产量")
    yield_unit: Optional[CropUnit] = None
    notes: Optional[str] = Field(None, max_length=500)


class CropResponse(CropBase):
    """粮食响应Schema"""
    id: int
    actual_harvest_date: Optional[date] = None
    total_yield: float
    status: CropStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class YieldRecordResponse(BaseModel):
    """产量记录响应Schema"""
    id: int
    record_date: date
    quantity: float
    unit: Optional[str] = None
    area_harvested: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class CropListResponse(BaseModel):
    """粮食列表响应"""
    items: list[CropResponse]
    total: int
    skip: int
    limit: int
