<template>
  <div class="statistics-view">
    <header class="header">
      <h1>大噜农场展示系统</h1>
      <nav class="nav">
        <router-link to="/" class="nav-link">仪表盘</router-link>
        <router-link to="/crops" class="nav-link">粮食管理</router-link>
        <router-link to="/animals" class="nav-link">动物管理</router-link>
        <router-link to="/flowers" class="nav-link">花卉管理</router-link>
        <router-link to="/statistics" class="nav-link">统计分析</router-link>
      </nav>
    </header>

    <main class="main">
      <h2>统计分析</h2>

      <div class="charts-grid">
        <div class="chart-card">
          <h3>各品种粮食产量</h3>
          <div ref="cropChartRef" class="chart"></div>
        </div>
        <div class="chart-card">
          <h3>粮食状态分布</h3>
          <div ref="statusChartRef" class="chart"></div>
        </div>
        <div class="chart-card">
          <h3>动物按产品类型</h3>
          <div ref="animalChartRef" class="chart"></div>
        </div>
        <div class="chart-card">
          <h3>花卉按季节分布</h3>
          <div ref="flowerChartRef" class="chart"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import * as echarts from 'echarts'

const statisticsStore = useStatisticsStore()
const cropChartRef = ref<HTMLElement>()
const statusChartRef = ref<HTMLElement>()
const animalChartRef = ref<HTMLElement>()
const flowerChartRef = ref<HTMLElement>()

onMounted(async () => {
  await statisticsStore.fetchChartData()
  initCharts()
})

function initCharts() {
  const data = statisticsStore.chartData
  if (!data) return

  // 粮食产量柱状图
  if (cropChartRef.value) {
    const cropChart = echarts.init(cropChartRef.value)
    cropChart.setOption({
      title: { text: data.crop_yield_by_variety.title },
      tooltip: {},
      xAxis: { data: data.crop_yield_by_variety.labels },
      yAxis: {},
      series: [{
        type: 'bar',
        data: data.crop_yield_by_variety.datasets[0]?.data || [],
        itemStyle: { color: '#4CAF50' }
      }]
    })
  }

  // 粮食状态饼图
  if (statusChartRef.value) {
    const statusChart = echarts.init(statusChartRef.value)
    statusChart.setOption({
      title: { text: data.crop_status_pie.title },
      tooltip: {},
      series: [{
        type: 'pie',
        data: data.crop_status_pie.labels.map((label, i) => ({
          name: label,
          value: data.crop_status_pie.datasets[0]?.data[i] || 0
        }))
      }]
    })
  }

  // 动物类型饼图
  if (animalChartRef.value) {
    const animalChart = echarts.init(animalChartRef.value)
    animalChart.setOption({
      title: { text: data.animal_by_product.title },
      tooltip: {},
      series: [{
        type: 'pie',
        data: data.animal_by_product.labels.map((label, i) => ({
          name: label,
          value: data.animal_by_product.datasets[0]?.data[i] || 0
        }))
      }]
    })
  }

  // 花卉季节柱状图
  if (flowerChartRef.value) {
    const flowerChart = echarts.init(flowerChartRef.value)
    flowerChart.setOption({
      title: { text: data.flower_by_season.title },
      tooltip: {},
      xAxis: { data: data.flower_by_season.labels },
      yAxis: {},
      series: [{
        type: 'bar',
        data: data.flower_by_season.datasets[0]?.data || [],
        itemStyle: { color: '#FF9800' }
      }]
    })
  }
}
</script>

<style scoped>
.statistics-view {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background-color: #4CAF50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 1.5rem;
  margin: 0;
}

.nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.main {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.chart-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 1rem;
}

.chart {
  width: 100%;
  height: 300px;
}
</style>
