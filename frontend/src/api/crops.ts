import apiClient from './client'
import type {
  Crop,
  CropCreate,
  CropUpdate,
  CropListParams,
  CropListResponse,
  CropHarvest
} from '@/types/crop'

export const cropsApi = {
  // 获取粮食列表
  getList: async (params: CropListParams = {}): Promise<CropListResponse> => {
    const response = await apiClient.get<CropListResponse>('/crops', { params })
    return response.data
  },

  // 获取单个粮食
  getById: async (id: number): Promise<Crop> => {
    const response = await apiClient.get<Crop>(`/crops/${id}`)
    return response.data
  },

  // 创建粮食
  create: async (data: CropCreate): Promise<Crop> => {
    const response = await apiClient.post<Crop>('/crops', data)
    return response.data
  },

  // 更新粮食
  update: async (id: number, data: CropUpdate): Promise<Crop> => {
    const response = await apiClient.put<Crop>(`/crops/${id}`, data)
    return response.data
  },

  // 删除粮食
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/crops/${id}`)
  },

  // 标记为已收获
  harvest: async (id: number, data: CropHarvest): Promise<Crop> => {
    const response = await apiClient.patch<Crop>(`/crops/${id}/harvest`, data)
    return response.data
  }
}
