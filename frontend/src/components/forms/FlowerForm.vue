<template>
  <form @submit.prevent="handleSubmit" class="form">
    <div class="form-group">
      <label class="form-label required">名称</label>
      <input
        v-model="formData.name"
        type="text"
        class="form-input"
        :class="{ 'input-error': errors.name }"
        placeholder="如：玫瑰"
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
        placeholder="如：红玫瑰"
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
      <label class="form-label required">种植日期</label>
      <input
        v-model="formData.plant_date"
        type="date"
        class="form-input"
        :class="{ 'input-error': errors.plant_date }"
      />
      <span v-if="errors.plant_date" class="error-text">{{ errors.plant_date }}</span>
    </div>

    <div class="form-group">
      <label class="form-label">开花季节</label>
      <select v-model="formData.bloom_season" class="form-select">
        <option value="">请选择</option>
        <option value="spring">春季</option>
        <option value="summer">夏季</option>
        <option value="autumn">秋季</option>
        <option value="winter">冬季</option>
        <option value="all_year">全年</option>
        <option value="multiple">多季节</option>
      </select>
    </div>

    <div class="form-group">
      <label class="form-label">颜色</label>
      <div class="color-inputs">
        <div
          v-for="(color, index) in colorList"
          :key="index"
          class="color-item"
        >
          <input
            v-model="colorList[index]"
            type="text"
            class="form-input"
            placeholder="如：红色"
          />
          <button
            type="button"
            class="btn-icon btn-remove"
            @click="removeColor(index)"
            v-if="colorList.length > 1"
          >&times;</button>
        </div>
        <button type="button" class="btn btn-sm btn-add" @click="addColor">
          + 添加颜色
        </button>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">用途</label>
      <select v-model="formData.purpose" class="form-select">
        <option value="">请选择</option>
        <option value="ornamental">观赏</option>
        <option value="sale">销售</option>
        <option value="essential_oil">精油</option>
        <option value="medicinal">药用</option>
        <option value="other">其他</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group half">
        <label class="form-label">预估产量</label>
        <input
          v-model.number="formData.estimated_yield"
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
          placeholder="如：支"
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
import { useFlowersStore } from '@/stores/flowers'
import type { FlowerCreate } from '@/types/flower'

const emit = defineEmits<{
  success: []
  cancel: []
}>()

const flowersStore = useFlowersStore()

const formData = reactive<FlowerCreate>({
  name: '',
  variety: '',
  quantity: 0,
  plant_date: '',
  bloom_season: undefined,
  colors: [],
  purpose: undefined,
  estimated_yield: undefined,
  yield_unit: undefined,
  notes: undefined
})

const colorList = ref<string[]>([''])

function addColor() {
  colorList.value.push('')
}

function removeColor(index: number) {
  colorList.value.splice(index, 1)
}

function syncColors() {
  const validColors = colorList.value.filter(c => c.trim())
  formData.colors = validColors.length > 0 ? validColors : undefined
}

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

  if (!formData.plant_date) {
    errors.plant_date = '请选择种植日期'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  if (!validate()) return

  syncColors()

  loading.value = true
  submitError.value = null

  try {
    await flowersStore.createFlower(formData)
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

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.btn-add {
  background-color: #e0f2fe;
  color: #0369a1;
  align-self: flex-start;
}

.btn-add:hover {
  background-color: #bae6fd;
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

.color-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.color-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.color-item .form-input {
  flex: 1;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #9ca3af;
  padding: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  color: #ef4444;
}
</style>
