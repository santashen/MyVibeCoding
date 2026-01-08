import { defineStore } from 'pinia'
import { ref } from 'vue'
import { animalsApi, type Animal, type AnimalCreate, type AnimalUpdate } from '@/api/animals'

export const useAnimalsStore = defineStore('animals', () => {
  const animals = ref<Animal[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAnimals() {
    loading.value = true
    error.value = null
    try {
      const response = await animalsApi.getList()
      animals.value = response.items
      total.value = response.total
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createAnimal(data: AnimalCreate) {
    loading.value = true
    try {
      const newAnimal = await animalsApi.create(data)
      animals.value.unshift(newAnimal)
      total.value++
      return newAnimal
    } finally {
      loading.value = false
    }
  }

  async function updateAnimal(id: number, data: AnimalUpdate) {
    loading.value = true
    try {
      const updated = await animalsApi.update(id, data)
      const index = animals.value.findIndex(a => a.id === id)
      if (index !== -1) {
        animals.value[index] = updated
      }
      return updated
    } finally {
      loading.value = false
    }
  }

  async function deleteAnimal(id: number) {
    loading.value = true
    try {
      await animalsApi.delete(id)
      animals.value = animals.value.filter(a => a.id !== id)
      total.value--
    } finally {
      loading.value = false
    }
  }

  function reset() {
    animals.value = []
    total.value = 0
    error.value = null
  }

  return {
    animals,
    total,
    loading,
    error,
    fetchAnimals,
    createAnimal,
    updateAnimal,
    deleteAnimal,
    reset
  }
})
