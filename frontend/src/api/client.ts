import axios, { type AxiosInstance, type AxiosError, type InternalAxiosRequestConfig } from 'axios'

// API响应类型
export interface ApiResponse<T> {
  data: T
}

// API错误类型
export interface ApiError {
  detail: string
  status: number
}

// 创建Axios实例

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
    }
    return Promise.reject(error)
  }
)

export default apiClient
