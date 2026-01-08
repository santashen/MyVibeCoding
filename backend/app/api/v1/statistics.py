from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.schemas.statistics import (
    OverviewStats, CropStats, AnimalStats, FlowerStats,
    ChartDataResponse, CalendarData
)
from app.models import Crop, Animal, Flower, CropStatus

router = APIRouter()


@router.get("/overview", response_model=OverviewStats)
def get_overview_stats(db: Session = Depends(get_db)):
    """获取总览统计数据"""
    # 粮食统计
    total_crops = db.query(func.count(Crop.id)).scalar()
    growing_crops = db.query(func.count(Crop.id)).filter(Crop.status == CropStatus.GROWING).scalar()
    harvested_crops = db.query(func.count(Crop.id)).filter(Crop.status == CropStatus.HARVESTED).scalar()
    total_crop_yield = db.query(func.sum(Crop.total_yield)).scalar() or 0

    # 动物统计
    total_animal_varieties = db.query(func.count(func.distinct(Animal.variety))).scalar()
    total_animals = db.query(func.sum(Animal.quantity)).scalar() or 0
    estimated_daily_yield = db.query(func.sum(Animal.estimated_daily_yield)).scalar() or 0

    # 花卉统计
    total_flower_varieties = db.query(func.count(func.distinct(Flower.variety))).scalar()
    total_flowers = db.query(func.sum(Flower.quantity)).scalar() or 0

    return {
        "total_crops": total_crops or 0,
        "growing_crops": growing_crops or 0,
        "harvested_crops": harvested_crops or 0,
        "total_crop_yield": float(total_crop_yield),
        "total_animal_varieties": total_animal_varieties or 0,
        "total_animals": int(total_animals),
        "estimated_daily_yield": float(estimated_daily_yield),
        "total_flower_varieties": total_flower_varieties or 0,
        "total_flowers": int(total_flowers),
    }


@router.get("/crops", response_model=CropStats)
def get_crop_statistics(db: Session = Depends(get_db)):
    """获取粮食统计数据"""
    # 按品种分组产量
    by_variety = dict(
        db.query(Crop.variety, func.sum(Crop.total_yield))
        .group_by(Crop.variety)
        .all()
    )

    # 按状态分组数量
    by_status = dict(
        db.query(Crop.status, func.count(Crop.id))
        .group_by(Crop.status)
        .all()
    )
    # 转换枚举为字符串
    by_status = {s.value if hasattr(s, 'value') else str(s): c for s, c in by_status.items()}

    return {
        "by_variety": {k: float(v) for k, v in by_variety.items()},
        "by_status": by_status,
    }


@router.get("/animals", response_model=AnimalStats)
def get_animal_statistics(db: Session = Depends(get_db)):
    """获取动物统计数据"""
    # 按产品类型分组数量
    by_product_type = dict(
        db.query(Animal.product_type, func.sum(Animal.quantity))
        .group_by(Animal.product_type)
        .all()
    )
    by_product_type = {str(k): int(v) for k, v in by_product_type.items() if k is not None}

    # 按品种分组数量
    by_variety = dict(
        db.query(Animal.variety, func.sum(Animal.quantity))
        .group_by(Animal.variety)
        .all()
    )

    return {
        "by_product_type": by_product_type,
        "by_variety": {k: int(v) for k, v in by_variety.items()},
    }


@router.get("/flowers", response_model=FlowerStats)
def get_flower_statistics(db: Session = Depends(get_db)):
    """获取花卉统计数据"""
    # 按季节分组数量
    by_season = dict(
        db.query(Flower.bloom_season, func.sum(Flower.quantity))
        .group_by(Flower.bloom_season)
        .all()
    )
    by_season = {str(k): int(v) for k, v in by_season.items() if k is not None}

    # 按用途分组数量
    by_purpose = dict(
        db.query(Flower.purpose, func.sum(Flower.quantity))
        .group_by(Flower.purpose)
        .all()
    )
    by_purpose = {str(k): int(v) for k, v in by_purpose.items() if k is not None}

    return {
        "by_season": by_season,
        "by_purpose": by_purpose,
    }


@router.get("/charts", response_model=ChartDataResponse)
def get_chart_data(db: Session = Depends(get_db)):
    """获取图表数据汇总"""
    # 粮食按品种产量
    crop_variety_data = db.query(Crop.variety, func.sum(Crop.total_yield)).group_by(Crop.variety).all()
    crop_yield_by_variety = {
        "title": "各品种粮食产量",
        "type": "bar",
        "labels": [v for v, _ in crop_variety_data],
        "datasets": [{"data": [float(y) for _, y in crop_variety_data]}]
    }

    # 粮食状态饼图
    crop_status_data = db.query(Crop.status, func.count(Crop.id)).group_by(Crop.status).all()
    crop_status_pie = {
        "title": "粮食状态分布",
        "type": "pie",
        "labels": [str(s) for s, _ in crop_status_data],
        "datasets": [{"data": [c for _, c in crop_status_data]}]
    }

    # 动物按产品类型
    animal_type_data = db.query(Animal.product_type, func.sum(Animal.quantity)).group_by(Animal.product_type).all()
    animal_by_product = {
        "title": "动物按产品类型分布",
        "type": "pie",
        "labels": [str(t) for t, _ in animal_type_data if t is not None],
        "datasets": [{"data": [int(q) for _, q in animal_type_data if _ is not None]}]
    }

    # 花卉按季节
    flower_season_data = db.query(Flower.bloom_season, func.sum(Flower.quantity)).group_by(Flower.bloom_season).all()
    flower_by_season = {
        "title": "花卉按开花季节分布",
        "type": "bar",
        "labels": [str(s) for s, _ in flower_season_data if s is not None],
        "datasets": [{"data": [int(q) for _, q in flower_season_data if _ is not None]}]
    }

    return {
        "crop_yield_by_variety": crop_yield_by_variety,
        "crop_status_pie": crop_status_pie,
        "animal_by_product": animal_by_product,
        "flower_by_season": flower_by_season,
    }


@router.get("/calendar", response_model=CalendarData)
def get_calendar_data(
    year: int = 2024,
    db: Session = Depends(get_db)
):
    """获取日历数据"""
    events = []

    # 粮食种植和收获事件
    crops = db.query(Crop).all()
    for crop in crops:
        events.append({
            "date": crop.plant_date.isoformat(),
            "title": f"种植 {crop.name}",
            "type": "plant",
            "category": "crop",
            "count": 1
        })
        if crop.expected_harvest_date:
            events.append({
                "date": crop.expected_harvest_date.isoformat(),
                "title": f"预计收获 {crop.name}",
                "type": "harvest",
                "category": "crop",
                "count": 1
            })
        if crop.actual_harvest_date:
            events.append({
                "date": crop.actual_harvest_date.isoformat(),
                "title": f"收获 {crop.name}",
                "type": "harvest",
                "category": "crop",
                "count": 1
            })

    # 花卉种植事件
    flowers_data = db.query(Flower).all()
    for flower in flowers_data:
        events.append({
            "date": flower.plant_date.isoformat(),
            "title": f"种植 {flower.name}",
            "type": "plant",
            "category": "flower",
            "count": 1
        })

    return {"events": events}
