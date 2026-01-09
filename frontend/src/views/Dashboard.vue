<template>
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
