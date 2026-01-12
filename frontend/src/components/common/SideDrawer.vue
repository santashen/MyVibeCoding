<template>
  <div v-if="modelValue" class="drawer-overlay" @click="close">
    <div
      class="drawer-container"
      :class="{ 'drawer-open': modelValue }"
      @click.stop
    >
    <div class="drawer-header">
      <h3>{{ title }}</h3>
      <button class="close-btn" @click="close">&times;</button>
    </div>

    <div class="drawer-body">
      <slot></slot>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean
  title?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.drawer-container {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 500px;
  max-width: 90vw;
  background: white;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.drawer-open {
  transform: translateX(0);
}

.drawer-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #333;
}

.drawer-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.15s, color 0.15s;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #333;
}
</style>
