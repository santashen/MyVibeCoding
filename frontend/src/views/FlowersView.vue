<template>
  <main class="main">
      <div class="page-header">
        <h2>花卉管理</h2>
        <button class="btn btn-primary" @click="drawerOpen = true">添加花卉</button>
      </div>

      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>名称</th>
              <th>品种</th>
              <th>数量</th>
              <th>种植日期</th>
              <th>开花季节</th>
              <th>用途</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="flower in flowersStore.flowers" :key="flower.id">
              <td>{{ flower.name }}</td>
              <td>{{ flower.variety }}</td>
              <td>{{ flower.quantity }}</td>
              <td>{{ flower.plant_date }}</td>
              <td>{{ flower.bloom_season || '-' }}</td>
              <td>{{ flower.purpose || '-' }}</td>
            </tr>
            <tr v-if="flowersStore.flowers.length === 0">
              <td colspan="6" class="text-center">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <SideDrawer v-model="drawerOpen" title="添加花卉">
        <FlowerForm @success="handleSuccess" @cancel="drawerOpen = false" />
      </SideDrawer>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useFlowersStore } from '@/stores/flowers'
import SideDrawer from '@/components/common/SideDrawer.vue'
import FlowerForm from '@/components/forms/FlowerForm.vue'

const flowersStore = useFlowersStore()
const drawerOpen = ref(false)

onMounted(() => {
  flowersStore.fetchFlowers()
})

function handleSuccess() {
  drawerOpen.value = false
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

.text-center {
  text-align: center;
  color: #999;
}
</style>
