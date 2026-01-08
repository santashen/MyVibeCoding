import { defineStore } from 'pinia'
import { ref } from 'vue'
import { statisticsApi, type OverviewStats, type ChartDataResponse } from '@/api/statistics'

export const useStatisticsStore = defineStore('statistics', () => {
  const overview = ref<OverviewStats | null>(null)
  const chartData = ref<ChartDataResponse | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchOverview() {
    loading.value = true
    error.value = null
    try {
      overview.value = await statisticsApi.getOverview()
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取统计数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchChartData() {
    loading.value = true
    error.value = null
    try {
      chartData.value = await statisticsApi.getCharts()
    } catch (err: any) {
      error.value = err.response?.data?.detail || '获取图表数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function reset() {
    overview.value = null
    chartData.value = null
    error.value = null
  }

  return {
    overview,
    chartData,
    loading,
    error,
    fetchOverview,
    fetchChartData,
    reset
  }
})
