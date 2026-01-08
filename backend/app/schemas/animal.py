from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class ProductType(str, Enum):
    MILK = "milk"
    EGG = "egg"
    WOOL = "wool"
    MEAT = "meat"
    HONEY = "honey"
    OTHER = "other"


class AnimalBase(BaseModel):
    """动物基础Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="动物名称")
    variety: str = Field(..., min_length=1, max_length=100, description="品种")
    quantity: int = Field(..., ge=0, description="数量")
    acquire_date: date = Field(..., description="购入/出生日期")
    product_type: Optional[ProductType] = Field(None, description="产产品类型")
    estimated_daily_yield: Optional[float] = Field(None, ge=0, description="预估日产产量")
    yield_unit: Optional[str] = Field(None, max_length=20, description="产量单位")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class AnimalCreate(AnimalBase):
    """创建动物Schema"""
    pass


class AnimalUpdate(BaseModel):
    """更新动物Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    variety: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    acquire_date: Optional[date] = None
    product_type: Optional[ProductType] = None
    estimated_daily_yield: Optional[float] = Field(None, ge=0)
    yield_unit: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)


class AnimalResponse(AnimalBase):
    """动物响应Schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnimalListResponse(BaseModel):
    """动物列表响应"""
    items: list[AnimalResponse]
    total: int
    skip: int
    limit: int
