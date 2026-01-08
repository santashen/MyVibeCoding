from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.schemas.crop import (
    CropCreate, CropUpdate, CropResponse, CropListResponse,
    CropHarvestUpdate, CropStatus
)
from app.models import Crop

router = APIRouter()


@router.get("/", response_model=CropListResponse)
def get_crops(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态筛选"),
    sort_by: Optional[str] = Query("plant_date", description="排序字段"),
    sort_order: Optional[str] = Query("desc", description="排序方向: asc, desc"),
    db: Session = Depends(get_db)
):
    """获取粮食列表"""
    query = db.query(Crop)

    # 筛选
    if status_filter:
        try:
            status_enum = CropStatus(status_filter)
            query = query.filter(Crop.status == status_enum)
        except ValueError:
            pass

    # 排序
    order_column = getattr(Crop, sort_by, Crop.plant_date)
    if sort_order == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    # 分页
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
def create_crop(
    crop_data: CropCreate,
    db: Session = Depends(get_db)
):
    """创建新的粮食记录"""
    db_crop = Crop(**crop_data.model_dump())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop


@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """获取单个粮食详情"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="粮食记录不存在")
    return crop


@router.put("/{crop_id}", response_model=CropResponse)
def update_crop(
    crop_id: int,
    crop_data: CropUpdate,
    db: Session = Depends(get_db)
):
    """更新粮食记录"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="粮食记录不存在")

    update_data = crop_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(crop, field, value)

    db.commit()
    db.refresh(crop)
    return crop


@router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """删除粮食记录"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="粮食记录不存在")

    db.delete(crop)
    db.commit()
    return None


@router.patch("/{crop_id}/harvest", response_model=CropResponse)
def mark_as_harvested(
    crop_id: int,
    harvest_data: CropHarvestUpdate,
    db: Session = Depends(get_db)
):
    """标记粮食为已收获，并记录产量"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="粮食记录不存在")

    crop.actual_harvest_date = harvest_data.actual_harvest_date
    crop.total_yield = harvest_data.yield_quantity
    crop.status = CropStatus.HARVESTED

    if harvest_data.yield_unit:
        crop.unit = harvest_data.yield_unit

    db.commit()
    db.refresh(crop)
    return crop
