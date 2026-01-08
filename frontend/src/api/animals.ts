import apiClient from './client'
import type {
  Animal,
  AnimalCreate,
  AnimalUpdate
} from '@/types/animal'

interface AnimalListParams {
  skip?: number
  limit?: number
}

interface AnimalListResponse {
  items: Animal[]
  total: number
  skip: number
  limit: number
}

export const animalsApi = {
  // 获取动物列表
  getList: async (params: AnimalListParams = {}): Promise<AnimalListResponse> => {
    const response = await apiClient.get<AnimalListResponse>('/animals', { params })
    return response.data
  },

  // 获取单个动物
  getById: async (id: number): Promise<Animal> => {
    const response = await apiClient.get<Animal>(`/animals/${id}`)
    return response.data
  },

  // 创建动物
  create: async (data: AnimalCreate): Promise<Animal> => {
    const response = await apiClient.post<Animal>('/animals', data)
    return response.data
  },

  // 更新动物
  update: async (id: number, data: AnimalUpdate): Promise<Animal> => {
    const response = await apiClient.put<Animal>(`/animals/${id}`, data)
    return response.data
  },

  // 删除动物
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/animals/${id}`)
  }
}
