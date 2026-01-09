import { defineStore } from 'pinia'
import { ref } from 'vue'
import { flowersApi } from '@/api/flowers'
import type { Flower, FlowerCreate, FlowerUpdate } from '@/types/flower'

export const useFlowersStore = defineStore('flowers', () => {
  const flowers = ref<Flower[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchFlowers() {
    loading.value = true
    error.value = null
    try {
      const response = await flowersApi.getList()
      flowers.value = response.items
      total.value = response.total
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createFlower(data: FlowerCreate) {
    loading.value = true
    try {
      const newFlower = await flowersApi.create(data)
      flowers.value.unshift(newFlower)
      total.value++
      return newFlower
    } finally {
      loading.value = false
    }
  }

  async function updateFlower(id: number, data: FlowerUpdate) {
    loading.value = true
    try {
      const updated = await flowersApi.update(id, data)
      const index = flowers.value.findIndex(f => f.id === id)
      if (index !== -1) {
        flowers.value[index] = updated
      }
      return updated
    } finally {
      loading.value = false
    }
  }

  async function deleteFlower(id: number) {
    loading.value = true
    try {
      await flowersApi.delete(id)
      flowers.value = flowers.value.filter(f => f.id !== id)
      total.value--
    } finally {
      loading.value = false
    }
  }

  function reset() {
    flowers.value = []
    total.value = 0
    error.value = null
  }

  return {
    flowers,
    total,
    loading,
    error,
    fetchFlowers,
    createFlower,
    updateFlower,
    deleteFlower,
    reset
  }
})
