import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cropsApi } from '@/api/crops'
import type {
  Crop,
  CropCreate,
  CropUpdate,
  CropListParams
} from '@/types/crop'

export const useCropsStore = defineStore('crops', () => {
  const crops = ref<Crop[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const params = ref<CropListParams>({
    skip: 0,
    limit: 20,
    sort_by: 'plant_date',
    sort_order: 'desc'
  })

  const growingCrops = computed(() =>
    crops.value.filter(c => c.status === 'growing')
  )

  const harvestedCrops = computed(() =>
    crops.value.filter(c => c.status === 'harvested')
  )

  const totalYield = computed(() =>
    crops.value.reduce((sum, c) => sum + c.total_yield, 0)
  )

  async function fetchCrops() {
    loading.value = true
    error.value = null
    try {
      const response = await cropsApi.getList(params.value)
      crops.value = response.items
      total.value = response.total
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCrop(data: CropCreate) {
    loading.value = true
    try {
      const newCrop = await cropsApi.create(data)
      crops.value.unshift(newCrop)
      total.value++
      return newCrop
    } finally {
      loading.value = false
    }
  }

  async function updateCrop(id: number, data: CropUpdate) {
    loading.value = true
    try {
      const updated = await cropsApi.update(id, data)
      const index = crops.value.findIndex(c => c.id === id)
      if (index !== -1) {
        crops.value[index] = updated
      }
      return updated
    } finally {
      loading.value = false
    }
  }

  async function deleteCrop(id: number) {
    loading.value = true
    try {
      await cropsApi.delete(id)
      crops.value = crops.value.filter(c => c.id !== id)
      total.value--
    } finally {
      loading.value = false
    }
  }

  function setParams(newParams: Partial<CropListParams>) {
    params.value = { ...params.value, ...newParams }
  }

  function reset() {
    crops.value = []
    total.value = 0
    error.value = null
  }

  return {
    crops,
    total,
    loading,
    error,
    params,
    growingCrops,
    harvestedCrops,
    totalYield,
    fetchCrops,
    createCrop,
    updateCrop,
    deleteCrop,
    setParams,
    reset
  }
})
