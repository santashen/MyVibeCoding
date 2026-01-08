// 统计数据类型定义
export interface OverviewStats {
  total_crops: number
  growing_crops: number
  harvested_crops: number
  total_crop_yield: number
  total_animal_varieties: number
  total_animals: number
  estimated_daily_yield: number
  total_flower_varieties: number
  total_flowers: number
}

export interface CropStats {
  by_variety: Record<string, number>
  by_status: Record<string, number>
}

export interface AnimalStats {
  by_product_type: Record<string, number>
  by_variety: Record<string, number>
}

export interface FlowerStats {
  by_season: Record<string, number>
  by_purpose: Record<string, number>
}

export interface ChartData {
  title: string
  type: string
  labels: string[]
  datasets: Array<Record<string, unknown>>
}

export interface ChartDataResponse {
  crop_yield_by_variety: ChartData
  crop_status_pie: ChartData
  animal_by_product: ChartData
  flower_by_season: ChartData
}

export interface CalendarEvent {
  date: string
  title: string
  type: string
  category: string
  count: number
}

export interface CalendarData {
  events: CalendarEvent[]
}
