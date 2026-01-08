// 动物类型定义
export enum ProductType {
  MILK = 'milk',
  EGG = 'egg',
  WOOL = 'wool',
  MEAT = 'meat',
  HONEY = 'honey',
  OTHER = 'other'
}

export interface Animal {
  id: number
  name: string
  variety: string
  quantity: number
  acquire_date: string
  product_type: ProductType | null
  estimated_daily_yield: number | null
  yield_unit: string | null
  notes: string | null
  created_at: string
  updated_at: string
}

export interface AnimalCreate {
  name: string
  variety: string
  quantity: number
  acquire_date: string
  product_type?: ProductType
  estimated_daily_yield?: number
  yield_unit?: string
  notes?: string
}

export interface AnimalUpdate {
  name?: string
  variety?: string
  quantity?: number
  acquire_date?: string
  product_type?: ProductType
  estimated_daily_yield?: number
  yield_unit?: string
  notes?: string
}

export interface AnimalListResponse {
  items: Animal[]
  total: number
  skip: number
  limit: number
}
