// 粮食类型定义
export enum CropStatus {
  GROWING = 'growing',
  HARVESTED = 'harvested',
  FAILED = 'failed'
}

export enum CropUnit {
  TON = 'ton',
  KG = 'kg',
  GRAM = 'gram'
}

export interface Crop {
  id: number
  name: string
  variety: string
  area: number
  plant_date: string
  expected_harvest_date: string | null
  actual_harvest_date: string | null
  total_yield: number
  unit: CropUnit
  status: CropStatus
  notes: string | null
  created_at: string
  updated_at: string
}

export interface CropCreate {
  name: string
  variety: string
  area: number
  plant_date: string
  expected_harvest_date?: string
  unit?: CropUnit
  notes?: string
}

export interface CropUpdate {
  name?: string
  variety?: string
  area?: number
  plant_date?: string
  expected_harvest_date?: string
  actual_harvest_date?: string
  total_yield?: number
  unit?: CropUnit
  status?: CropStatus
  notes?: string
}

export interface CropListParams {
  skip?: number
  limit?: number
  status?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface CropListResponse {
  items: Crop[]
  total: number
  skip: number
  limit: number
}

export interface CropHarvest {
  actual_harvest_date: string
  yield_quantity: number
  yield_unit?: CropUnit
  notes?: string
}
