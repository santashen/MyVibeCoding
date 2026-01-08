from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class FlowerPurpose(str, Enum):
    ORNAMENTAL = "ornamental"
    SALE = "sale"
    ESSENTIAL_OIL = "essential_oil"
    MEDICINAL = "medicinal"
    OTHER = "other"


class BloomSeason(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"
    ALL_YEAR = "all_year"
    MULTIPLE = "multiple"


class FlowerBase(BaseModel):
    """花卉基础Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="花卉名称")
    variety: str = Field(..., min_length=1, max_length=100, description="品种")
    quantity: int = Field(..., ge=0, description="数量")
    plant_date: date = Field(..., description="种植日期")
    bloom_season: Optional[BloomSeason] = Field(None, description="开花季节")
    colors: Optional[list[str]] = Field(None, description="颜色列表")
    purpose: Optional[FlowerPurpose] = Field(None, description="主要用途")
    estimated_yield: Optional[float] = Field(None, ge=0, description="预估产量")
    yield_unit: Optional[str] = Field(None, max_length=20, description="产量单位")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class FlowerCreate(FlowerBase):
    """创建花卉Schema"""
    pass


class FlowerUpdate(BaseModel):
    """更新花卉Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    variety: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    plant_date: Optional[date] = None
    bloom_season: Optional[BloomSeason] = None
    colors: Optional[list[str]] = None
    purpose: Optional[FlowerPurpose] = None
    estimated_yield: Optional[float] = Field(None, ge=0)
    yield_unit: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)


class FlowerResponse(FlowerBase):
    """花卉响应Schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FlowerListResponse(BaseModel):
    """花卉列表响应"""
    items: list[FlowerResponse]
    total: int
    skip: int
    limit: int
