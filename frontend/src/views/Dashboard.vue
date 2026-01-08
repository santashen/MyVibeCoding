<template>
  <div class="dashboard">
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
      <section class="stats-cards">
        <div class="stat-card">
          <h3>粮食总数</h3>
          <p class="stat-value">{{ overview?.total_crops || 0 }}</p>
          <p class="stat-label">生长中: {{ overview?.growing_crops || 0 }} | 已收获: {{ overview?.harvested_crops || 0 }}</p>
        </div>
        <div class="stat-card">
          <h3>动物总数</h3>
          <p class="stat-value">{{ overview?.total_animals || 0 }}</p>
          <p class="stat-label">品种数: {{ overview?.total_animal_varieties || 0 }}</p>
        </div>
        <div class="stat-card">
          <h3>花卉总数</h3>
          <p class="stat-value">{{ overview?.total_flowers || 0 }}</p>
          <p class="stat-label">品种数: {{ overview?.total_flower_varieties || 0 }}</p>
        </div>
        <div class="stat-card">
          <h3>总产量</h3>
          <p class="stat-value">{{ formatNumber(overview?.total_crop_yield || 0) }}</p>
          <p class="stat-label">千克</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'

const statisticsStore = useStatisticsStore()
const overview = ref(statisticsStore.overview)

onMounted(async () => {
  await statisticsStore.fetchOverview()
  overview.value = statisticsStore.overview
})

function formatNumber(num: number): string {
  return num.toFixed(1)
}
</script>

<style scoped>
.dashboard {
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

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #4CAF50;
  margin: 0 0 0.5rem 0;
}

.stat-label {
  color: #999;
  font-size: 0.85rem;
  margin: 0;
}
</style>
