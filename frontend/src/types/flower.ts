// 花卉类型定义
export enum FlowerPurpose {
  ORNAMENTAL = 'ornamental',
  SALE = 'sale',
  ESSENTIAL_OIL = 'essential_oil',
  MEDICINAL = 'medicinal',
  OTHER = 'other'
}

export enum BloomSeason {
  SPRING = 'spring',
  SUMMER = 'summer',
  AUTUMN = 'autumn',
  WINTER = 'winter',
  ALL_YEAR = 'all_year',
  MULTIPLE = 'multiple'
}

export interface Flower {
  id: number
  name: string
  variety: string
  quantity: number
  plant_date: string
  bloom_season: BloomSeason | null
  colors: string[] | null
  purpose: FlowerPurpose | null
  estimated_yield: number | null
  yield_unit: string | null
  notes: string | null
  created_at: string
  updated_at: string
}

export interface FlowerCreate {
  name: string
  variety: string
  quantity: number
  plant_date: string
  bloom_season?: BloomSeason
  colors?: string[]
  purpose?: FlowerPurpose
  estimated_yield?: number
  yield_unit?: string
  notes?: string
}

export interface FlowerUpdate {
  name?: string
  variety?: string
  quantity?: number
  plant_date?: string
  bloom_season?: BloomSeason
  colors?: string[]
  purpose?: FlowerPurpose
  estimated_yield?: number
  yield_unit?: string
  notes?: string
}

export interface FlowerListResponse {
  items: Flower[]
  total: number
  skip: number
  limit: number
}
