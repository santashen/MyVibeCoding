<template>
  <div id="app">
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
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script>

<style>
#app {
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
</style>
