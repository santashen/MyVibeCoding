import apiClient from './client'
import type {
  OverviewStats,
  CropStats,
  AnimalStats,
  FlowerStats,
  ChartDataResponse,
  CalendarData
} from '@/types/statistics'

export const statisticsApi = {
  // 获取总览统计
  getOverview: async (): Promise<OverviewStats> => {
    const response = await apiClient.get<OverviewStats>('/statistics/overview')
    return response.data
  },

  // 获取粮食统计
  getCrops: async (): Promise<CropStats> => {
    const response = await apiClient.get<CropStats>('/statistics/crops')
    return response.data
  },

  // 获取动物统计
  getAnimals: async (): Promise<AnimalStats> => {
    const response = await apiClient.get<AnimalStats>('/statistics/animals')
    return response.data
  },

  // 获取花卉统计
  getFlowers: async (): Promise<FlowerStats> => {
    const response = await apiClient.get<FlowerStats>('/statistics/flowers')
    return response.data
  },

  // 获取图表数据
  getCharts: async (): Promise<ChartDataResponse> => {
    const response = await apiClient.get<ChartDataResponse>('/statistics/charts')
    return response.data
  },

  // 获取日历数据
  getCalendar: async (year: number = 2024): Promise<CalendarData> => {
    const response = await apiClient.get<CalendarData>('/statistics/calendar', {
      params: { year }
    })
    return response.data
  }
}
