<template>
  <div class="animals-view">
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
      <div class="page-header">
        <h2>动物管理</h2>
        <button class="btn btn-primary">添加动物</button>
      </div>

      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>名称</th>
              <th>品种</th>
              <th>数量</th>
              <th>购入日期</th>
              <th>产品类型</th>
              <th>预估日产量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="animal in animalsStore.animals" :key="animal.id">
              <td>{{ animal.name }}</td>
              <td>{{ animal.variety }}</td>
              <td>{{ animal.quantity }}</td>
              <td>{{ animal.acquire_date }}</td>
              <td>{{ animal.product_type || '-' }}</td>
              <td>{{ animal.estimated_daily_yield || '-' }} {{ animal.yield_unit || '' }}</td>
            </tr>
            <tr v-if="animalsStore.animals.length === 0">
              <td colspan="6" class="text-center">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAnimalsStore } from '@/stores/animals'

const animalsStore = useAnimalsStore()

onMounted(() => {
  animalsStore.fetchAnimals()
})
</script>

<style scoped>
.animals-view {
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
