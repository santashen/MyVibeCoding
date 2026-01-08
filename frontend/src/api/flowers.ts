import apiClient from './client'
import type {
  Flower,
  FlowerCreate,
  FlowerUpdate
} from '@/types/flower'

interface FlowerListParams {
  skip?: number
  limit?: number
}

interface FlowerListResponse {
  items: Flower[]
  total: number
  skip: number
  limit: number
}

export const flowersApi = {
  // 获取花卉列表
  getList: async (params: FlowerListParams = {}): Promise<FlowerListResponse> => {
    const response = await apiClient.get<FlowerListResponse>('/flowers', { params })
    return response.data
  },

  // 获取单个花卉
  getById: async (id: number): Promise<Flower> => {
    const response = await apiClient.get<Flower>(`/flowers/${id}`)
    return response.data
  },

  // 创建花卉
  create: async (data: FlowerCreate): Promise<Flower> => {
    const response = await apiClient.post<Flower>('/flowers', data)
    return response.data
  },

  // 更新花卉
  update: async (id: number, data: FlowerUpdate): Promise<Flower> => {
    const response = await apiClient.put<Flower>(`/flowers/${id}`, data)
    return response.data
  },

  // 删除花卉
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/flowers/${id}`)
  }
}
