<template>
  <form @submit.prevent="handleSubmit" class="form">
    <div class="form-group">
      <label class="form-label required">名称</label>
      <input
        v-model="formData.name"
        type="text"
        class="form-input"
        :class="{ 'input-error': errors.name }"
        placeholder="如：奶牛"
      />
      <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
    </div>

    <div class="form-group">
      <label class="form-label required">品种</label>
      <input
        v-model="formData.variety"
        type="text"
        class="form-input"
        :class="{ 'input-error': errors.variety }"
        placeholder="如：荷斯坦"
      />
      <span v-if="errors.variety" class="error-text">{{ errors.variety }}</span>
    </div>

    <div class="form-group">
      <label class="form-label required">数量</label>
      <input
        v-model.number="formData.quantity"
        type="number"
        min="1"
        class="form-input"
        :class="{ 'input-error': errors.quantity }"
        placeholder="0"
      />
      <span v-if="errors.quantity" class="error-text">{{ errors.quantity }}</span>
    </div>

    <div class="form-group">
      <label class="form-label required">购入日期</label>
      <input
        v-model="formData.acquire_date"
        type="date"
        class="form-input"
        :class="{ 'input-error': errors.acquire_date }"
      />
      <span v-if="errors.acquire_date" class="error-text">{{ errors.acquire_date }}</span>
    </div>

    <div class="form-group">
      <label class="form-label">产品类型</label>
      <select v-model="formData.product_type" class="form-select">
        <option value="">请选择</option>
        <option value="milk">牛奶</option>
        <option value="egg">蛋类</option>
        <option value="wool">羊毛</option>
        <option value="meat">肉类</option>
        <option value="honey">蜂蜜</option>
        <option value="other">其他</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group half">
        <label class="form-label">预估日产量</label>
        <input
          v-model.number="formData.estimated_daily_yield"
          type="number"
          min="0"
          step="0.01"
          class="form-input"
          placeholder="0.00"
        />
      </div>

      <div class="form-group half">
        <label class="form-label">产量单位</label>
        <input
          v-model="formData.yield_unit"
          type="text"
          class="form-input"
          placeholder="如：kg"
        />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">备注</label>
      <textarea
        v-model="formData.notes"
        class="form-textarea"
        rows="3"
        placeholder="可选填备注信息..."
      ></textarea>
    </div>

    <div class="form-actions">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        取消
      </button>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? '保存中...' : '保存' }}
      </button>
    </div>

    <div v-if="submitError" class="alert alert-error">
      {{ submitError }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAnimalsStore } from '@/stores/animals'
import type { AnimalCreate } from '@/types/animal'

const emit = defineEmits<{
  success: []
  cancel: []
}>()

const animalsStore = useAnimalsStore()

const formData = reactive<AnimalCreate>({
  name: '',
  variety: '',
  quantity: 0,
  acquire_date: '',
  product_type: undefined,
  estimated_daily_yield: undefined,
  yield_unit: undefined,
  notes: undefined
})

const errors = reactive<Record<string, string>>({})
const submitError = ref<string | null>(null)
const loading = ref(false)

function validate(): boolean {
  Object.keys(errors).forEach(key => delete errors[key])

  let isValid = true

  if (!formData.name?.trim()) {
    errors.name = '请输入名称'
    isValid = false
  }

  if (!formData.variety?.trim()) {
    errors.variety = '请输入品种'
    isValid = false
  }

  if (!formData.quantity || formData.quantity <= 0) {
    errors.quantity = '请输入有效的数量'
    isValid = false
  }

  if (!formData.acquire_date) {
    errors.acquire_date = '请选择购入日期'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  if (!validate()) return

  loading.value = true
  submitError.value = null

  try {
    await animalsStore.createAnimal(formData)
    emit('success')
  } catch (err: any) {
    submitError.value = err.response?.data?.detail || '保存失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.half {
  flex: 1;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-label.required::after {
  content: ' *';
  color: #ef4444;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.875rem;
  transition: border-color 0.15s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.form-input.input-error {
  border-color: #ef4444;
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
}

.error-text {
  font-size: 0.75rem;
  color: #ef4444;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
  transition: background-color 0.15s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #45a049;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background-color: #e5e7eb;
}

.alert {
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.alert-error {
  background-color: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}
</style>
