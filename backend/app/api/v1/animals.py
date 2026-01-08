from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.animal import (
    AnimalCreate, AnimalUpdate, AnimalResponse, AnimalListResponse
)
from app.models import Animal

router = APIRouter()


@router.get("/", response_model=AnimalListResponse)
def get_animals(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db)
):
    """获取动物列表"""
    query = db.query(Animal).order_by(Animal.acquire_date.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(
    animal_data: AnimalCreate,
    db: Session = Depends(get_db)
):
    """创建新的动物记录"""
    db_animal = Animal(**animal_data.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    """获取单个动物详情"""
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="动物记录不存在")
    return animal


@router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal(
    animal_id: int,
    animal_data: AnimalUpdate,
    db: Session = Depends(get_db)
):
    """更新动物记录"""
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="动物记录不存在")

    update_data = animal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(animal, field, value)

    db.commit()
    db.refresh(animal)
    return animal


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    """删除动物记录"""
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="动物记录不存在")

    db.delete(animal)
    db.commit()
    return None
