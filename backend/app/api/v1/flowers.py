from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.flower import (
    FlowerCreate, FlowerUpdate, FlowerResponse, FlowerListResponse
)
from app.models import Flower

router = APIRouter()


@router.get("/", response_model=FlowerListResponse)
def get_flowers(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db)
):
    """获取花卉列表"""
    query = db.query(Flower).order_by(Flower.plant_date.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=FlowerResponse, status_code=status.HTTP_201_CREATED)
def create_flower(
    flower_data: FlowerCreate,
    db: Session = Depends(get_db)
):
    """创建新的花卉记录"""
    db_flower = Flower(**flower_data.model_dump())
    db.add(db_flower)
    db.commit()
    db.refresh(db_flower)
    return db_flower


@router.get("/{flower_id}", response_model=FlowerResponse)
def get_flower(flower_id: int, db: Session = Depends(get_db)):
    """获取单个花卉详情"""
    flower = db.query(Flower).filter(Flower.id == flower_id).first()
    if not flower:
        raise HTTPException(status_code=404, detail="花卉记录不存在")
    return flower


@router.put("/{flower_id}", response_model=FlowerResponse)
def update_flower(
    flower_id: int,
    flower_data: FlowerUpdate,
    db: Session = Depends(get_db)
):
    """更新花卉记录"""
    flower = db.query(Flower).filter(Flower.id == flower_id).first()
    if not flower:
        raise HTTPException(status_code=404, detail="花卉记录不存在")

    update_data = flower_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(flower, field, value)

    db.commit()
    db.refresh(flower)
    return flower


@router.delete("/{flower_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    """删除花卉记录"""
    flower = db.query(Flower).filter(Flower.id == flower_id).first()
    if not flower:
        raise HTTPException(status_code=404, detail="花卉记录不存在")

    db.delete(flower)
    db.commit()
    return None
