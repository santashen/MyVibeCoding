<template>
  <main class="main">
      <div class="page-header">
        <h2>粮食管理</h2>
        <button class="btn btn-primary" @click="drawerOpen = true">添加粮食</button>
      </div>

      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>名称</th>
              <th>品种</th>
              <th>面积(亩)</th>
              <th>种植日期</th>
              <th>状态</th>
              <th>产量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="crop in cropsStore.crops" :key="crop.id">
              <td>{{ crop.name }}</td>
              <td>{{ crop.variety }}</td>
              <td>{{ crop.area }}</td>
              <td>{{ crop.plant_date }}</td>
              <td>
                <span :class="getStatusClass(crop.status)">
                  {{ getStatusText(crop.status) }}
                </span>
              </td>
              <td>{{ crop.total_yield }} {{ crop.unit }}</td>
            </tr>
            <tr v-if="cropsStore.crops.length === 0">
              <td colspan="6" class="text-center">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <SideDrawer v-model="drawerOpen" title="添加粮食">
        <CropForm @success="handleSuccess" @cancel="drawerOpen = false" />
      </SideDrawer>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useCropsStore } from '@/stores/crops'
import { CropStatus } from '@/types/crop'
import SideDrawer from '@/components/common/SideDrawer.vue'
import CropForm from '@/components/forms/CropForm.vue'

const cropsStore = useCropsStore()
const drawerOpen = ref(false)

onMounted(() => {
  cropsStore.fetchCrops()
})

function handleSuccess() {
  drawerOpen.value = false
}

function getStatusClass(status: CropStatus): string {
  const map = {
    [CropStatus.GROWING]: 'status-growing',
    [CropStatus.HARVESTED]: 'status-harvested',
    [CropStatus.FAILED]: 'status-failed'
  }
  return map[status] || ''
}

function getStatusText(status: CropStatus): string {
  const map = {
    [CropStatus.GROWING]: '生长中',
    [CropStatus.HARVESTED]: '已收获',
    [CropStatus.FAILED]: '失败'
  }
  return map[status] || status
}
</script>

<style scoped>
.main {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  background-color: #f9f9f9;
  font-weight: 600;
  color: #666;
}

.status-growing {
  color: #2196F3;
}

.status-harvested {
  color: #4CAF50;
}

.status-failed {
  color: #f44336;
}

.text-center {
  text-align: center;
  color: #999;
}
</style>
