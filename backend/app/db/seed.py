"""
种子数据模块
提供测试/演示用例数据
"""
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.crop import Crop, CropStatus, CropUnit
from app.models.animal import Animal, ProductType
from app.models.flower import Flower, FlowerPurpose, BloomSeason
from app.models.yield_record import YieldRecord


# ============================================
# 粮食种子数据 (5条)
# ============================================
CROP_SEEDS = [
    {
        "name": "水稻",
        "variety": "杂交稻汕优63",
        "area": 15.5,
        "plant_date": date(2024, 4, 15),
        "expected_harvest_date": date(2024, 9, 20),
        "actual_harvest_date": date(2024, 9, 18),
        "total_yield": 9300.0,
        "unit": CropUnit.KG,
        "status": CropStatus.HARVESTED,
        "notes": "今年气候适宜，产量稳定"
    },
    {
        "name": "小麦",
        "variety": "济麦22",
        "area": 22.0,
        "plant_date": date(2023, 10, 10),
        "expected_harvest_date": date(2024, 6, 5),
        "actual_harvest_date": date(2024, 6, 8),
        "total_yield": 13200.0,
        "unit": CropUnit.KG,
        "status": CropStatus.HARVESTED,
        "notes": "遭受轻微干旱，影响不大"
    },
    {
        "name": "玉米",
        "variety": "郑单958",
        "area": 18.0,
        "plant_date": date(2024, 5, 20),
        "expected_harvest_date": date(2024, 9, 30),
        "total_yield": 0.0,
        "unit": CropUnit.KG,
        "status": CropStatus.GROWING,
        "notes": "长势良好，预计丰收"
    },
    {
        "name": "大豆",
        "variety": "黑农84",
        "area": 8.5,
        "plant_date": date(2024, 6, 5),
        "expected_harvest_date": date(2024, 10, 15),
        "total_yield": 0.0,
        "unit": CropUnit.KG,
        "status": CropStatus.GROWING,
        "notes": "与玉米间作种植"
    },
    {
        "name": "红薯",
        "variety": "徐薯32",
        "area": 5.0,
        "plant_date": date(2024, 3, 20),
        "expected_harvest_date": date(2024, 9, 1),
        "total_yield": 0.0,
        "unit": CropUnit.KG,
        "status": CropStatus.FAILED,
        "notes": "遭遇连续阴雨，根部腐烂"
    }
]


# ============================================
# 动物种子数据 (5条)
# ============================================
ANIMAL_SEEDS = [
    {
        "name": "奶牛",
        "variety": "荷斯坦奶牛",
        "quantity": 12,
        "acquire_date": date(2023, 3, 15),
        "product_type": ProductType.MILK,
        "estimated_daily_yield": 280.0,
        "yield_unit": "升",
        "notes": "健康状态良好"
    },
    {
        "name": "蛋鸡",
        "variety": "海兰褐",
        "quantity": 150,
        "acquire_date": date(2024, 1, 10),
        "product_type": ProductType.EGG,
        "estimated_daily_yield": 135.0,
        "yield_unit": "个",
        "notes": "产蛋率稳定在90%左右"
    },
    {
        "name": "绵羊",
        "variety": "美利奴羊",
        "quantity": 25,
        "acquire_date": date(2023, 6, 20),
        "product_type": ProductType.WOOL,
        "estimated_daily_yield": 0,
        "yield_unit": "千克",
        "notes": "每年剪毛两次"
    },
    {
        "name": "蜜蜂",
        "variety": "意大利蜂",
        "quantity": 30,
        "acquire_date": date(2024, 4, 1),
        "product_type": ProductType.HONEY,
        "estimated_daily_yield": 2.5,
        "yield_unit": "千克",
        "notes": "春季花期蜜源充足"
    },
    {
        "name": "肉兔",
        "variety": "新西兰兔",
        "quantity": 60,
        "acquire_date": date(2024, 2, 15),
        "product_type": ProductType.MEAT,
        "estimated_daily_yield": 0,
        "yield_unit": "千克",
        "notes": "计划3个月后出栏"
    }
]


# ============================================
# 花卉种子数据 (5条)
# ============================================
FLOWER_SEEDS = [
    {
        "name": "月季",
        "variety": "和平月季",
        "quantity": 200,
        "plant_date": date(2023, 11, 5),
        "bloom_season": BloomSeason.MULTIPLE,
        "bloom_seasons": ["spring", "summer", "autumn"],
        "colors": ["粉色", "白色", "黄色"],
        "purpose": FlowerPurpose.SALE,
        "estimated_yield": 1500,
        "yield_unit": "支/年",
        "notes": "温室栽培"
    },
    {
        "name": "薰衣草",
        "variety": "真薰衣草",
        "quantity": 500,
        "plant_date": date(2023, 9, 15),
        "bloom_season": BloomSeason.SUMMER,
        "bloom_seasons": ["summer"],
        "colors": ["紫色"],
        "purpose": FlowerPurpose.ESSENTIAL_OIL,
        "estimated_yield": 50,
        "yield_unit": "千克",
        "notes": "用于制作精油"
    },
    {
        "name": "牡丹",
        "variety": "洛阳红",
        "quantity": 80,
        "plant_date": date(2023, 10, 20),
        "bloom_season": BloomSeason.SPRING,
        "bloom_seasons": ["spring"],
        "colors": ["红色", "深红"],
        "purpose": FlowerPurpose.ORNAMENTAL,
        "estimated_yield": 0,
        "yield_unit": "支",
        "notes": "观赏为主，花期短"
    },
    {
        "name": "金银花",
        "variety": "大毛花",
        "quantity": 300,
        "plant_date": date(2024, 3, 10),
        "bloom_season": BloomSeason.ALL_YEAR,
        "bloom_seasons": ["spring", "summer", "autumn"],
        "colors": ["白色", "黄色"],
        "purpose": FlowerPurpose.MEDICINAL,
        "estimated_yield": 80,
        "yield_unit": "千克/年",
        "notes": "药用价值高"
    },
    {
        "name": "向日葵",
        "variety": "食用葵",
        "quantity": 1000,
        "plant_date": date(2024, 4, 20),
        "bloom_season": BloomSeason.SUMMER,
        "bloom_seasons": ["summer"],
        "colors": ["黄色"],
        "purpose": FlowerPurpose.OTHER,
        "estimated_yield": 150,
        "yield_unit": "千克",
        "notes": "收获葵花籽"
    }
]


# ============================================
# 产量记录种子数据 (4条，关联已收获的作物)
# ============================================
YIELD_RECORD_SEEDS = [
    {
        "record_date": date(2024, 9, 18),
        "quantity": 4800.0,
        "unit": "kg",
        "area_harvested": 8.0,
        "notes": "第一批收割"
    },
    {
        "record_date": date(2024, 9, 18),
        "quantity": 4500.0,
        "unit": "kg",
        "area_harvested": 7.5,
        "notes": "第二批收割"
    },
    {
        "record_date": date(2024, 6, 5),
        "quantity": 6800.0,
        "unit": "kg",
        "area_harvested": 12.0,
        "notes": "主产区收割"
    },
    {
        "record_date": date(2024, 6, 8),
        "quantity": 6400.0,
        "unit": "kg",
        "area_harvested": 10.0,
        "notes": "剩余区域收割"
    }
]


def seed_crops(db: Session) -> None:
    """插入粮食种子数据"""
    existing = db.query(Crop).count()
    if existing > 0:
        print(f"[Seed] 粮食数据已存在 ({existing} 条)，跳过")
        return

    for data in CROP_SEEDS:
        crop = Crop(**data)
        db.add(crop)
    db.commit()
    print(f"[Seed] 已创建 {len(CROP_SEEDS)} 条粮食数据")


def seed_animals(db: Session) -> None:
    """插入动物种子数据"""
    existing = db.query(Animal).count()
    if existing > 0:
        print(f"[Seed] 动物数据已存在 ({existing} 条)，跳过")
        return

    for data in ANIMAL_SEEDS:
        animal = Animal(**data)
        db.add(animal)
    db.commit()
    print(f"[Seed] 已创建 {len(ANIMAL_SEEDS)} 条动物数据")


def seed_flowers(db: Session) -> None:
    """插入花卉种子数据"""
    existing = db.query(Flower).count()
    if existing > 0:
        print(f"[Seed] 花卉数据已存在 ({existing} 条)，跳过")
        return

    for data in FLOWER_SEEDS:
        flower = Flower(**data)
        db.add(flower)
    db.commit()
    print(f"[Seed] 已创建 {len(FLOWER_SEEDS)} 条花卉数据")


def seed_yield_records(db: Session) -> None:
    """插入产量记录种子数据"""
    existing = db.query(YieldRecord).count()
    if existing > 0:
        print(f"[Seed] 产量记录已存在 ({existing} 条)，跳过")
        return

    # 获取已收获的粮食（水稻, 小麦）
    crops = db.query(Crop).filter(Crop.status == CropStatus.HARVESTED).all()

    if len(crops) >= 2:
        # 为第一条记录分配给水稻
        record1 = YieldRecord(crop_id=crops[0].id, **YIELD_RECORD_SEEDS[0])
        record2 = YieldRecord(crop_id=crops[0].id, **YIELD_RECORD_SEEDS[1])
        # 为第二条记录分配给小麦
        record3 = YieldRecord(crop_id=crops[1].id, **YIELD_RECORD_SEEDS[2])
        record4 = YieldRecord(crop_id=crops[1].id, **YIELD_RECORD_SEEDS[3])

        db.add_all([record1, record2, record3, record4])
        db.commit()
        print(f"[Seed] 已创建 4 条产量记录")
    else:
        print("[Seed] 没有找到已收获的粮食，跳过产量记录")


def seed_all(db: Session) -> None:
    """插入所有种子数据"""
    print("[Seed] 开始初始化种子数据...")
    seed_crops(db)
    seed_animals(db)
    seed_flowers(db)
    seed_yield_records(db)
    print("[Seed] 种子数据初始化完成")


def clear_seed_data(db: Session) -> None:
    """清除种子数据（仅开发环境使用）"""
    db.query(YieldRecord).delete()
    db.query(Crop).delete()
    db.query(Animal).delete()
    db.query(Flower).delete()
    db.commit()
    print("[Seed] 已清除所有种子数据")
