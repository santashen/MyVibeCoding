from pydantic import BaseModel
from typing import Dict, List, Optional


class OverviewStats(BaseModel):
    """总览统计"""
    # 粮食统计
    total_crops: int
    growing_crops: int
    harvested_crops: int
    total_crop_yield: float

    # 动物统计
    total_animal_varieties: int
    total_animals: int
    estimated_daily_yield: float

    # 花卉统计
    total_flower_varieties: int
    total_flowers: int


class CropStats(BaseModel):
    """粮食统计"""
    by_variety: Dict[str, float]  # 品种 -> 产量
    by_status: Dict[str, int]  # 状态 -> 数量


class AnimalStats(BaseModel):
    """动物统计"""
    by_product_type: Dict[str, int]  # 产品类型 -> 数量
    by_variety: Dict[str, int]  # 品种 -> 数量


class FlowerStats(BaseModel):
    """花卉统计"""
    by_season: Dict[str, int]  # 季节 -> 数量
    by_purpose: Dict[str, int]  # 用途 -> 数量


class ChartData(BaseModel):
    """图表数据格式"""
    title: str
    type: str  # bar, line, pie, etc.
    labels: List[str]
    datasets: List[Dict]


class ChartDataResponse(BaseModel):
    """图表数据汇总响应"""
    crop_yield_by_variety: ChartData
    crop_status_pie: ChartData
    animal_by_product: ChartData
    flower_by_season: ChartData


class CalendarEvent(BaseModel):
    """日历事件"""
    date: str
    title: str
    type: str  # plant, harvest, bloom
    category: str  # crop, animal, flower
    count: int


class CalendarData(BaseModel):
    """日历数据响应"""
    events: List[CalendarEvent]
