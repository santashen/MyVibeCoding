<template>
  <form @submit.prevent="handleSubmit" class="form">
    <div class="form-group">
      <label class="form-label required">名称</label>
      <input
        v-model="formData.name"
        type="text"
        class="form-input"
        :class="{ 'input-error': errors.name }"
        placeholder="如：水稻"
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
        placeholder="如：南粳46"
      />
      <span v-if="errors.variety" class="error-text">{{ errors.variety }}</span>
    </div>

    <div class="form-group">
      <label class="form-label required">种植面积（亩）</label>
      <input
        v-model.number="formData.area"
        type="number"
        step="0.01"
        min="0"
        class="form-input"
        :class="{ 'input-error': errors.area }"
        placeholder="0.00"
      />
      <span v-if="errors.area" class="error-text">{{ errors.area }}</span>
    </div>

    <div class="form-row">
      <div class="form-group half">
        <label class="form-label required">种植日期</label>
        <input
          v-model="formData.plant_date"
          type="date"
          class="form-input"
          :class="{ 'input-error': errors.plant_date }"
        />
        <span v-if="errors.plant_date" class="error-text">{{ errors.plant_date }}</span>
      </div>

      <div class="form-group half">
        <label class="form-label">预计收获日期</label>
        <input
          v-model="formData.expected_harvest_date"
          type="date"
          class="form-input"
          :min="formData.plant_date"
        />
        <span v-if="errors.expected_harvest_date" class="error-text">{{ errors.expected_harvest_date }}</span>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">产量单位</label>
      <select v-model="formData.unit" class="form-select">
        <option value="kg">千克</option>
        <option value="ton">吨</option>
        <option value="gram">克</option>
      </select>
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
import { useCropsStore } from '@/stores/crops'
import type { CropCreate } from '@/types/crop'
import { CropUnit } from '@/types/crop'

const emit = defineEmits<{
  success: []
  cancel: []
}>()

const cropsStore = useCropsStore()

const formData = reactive<CropCreate>({
  name: '',
  variety: '',
  area: 0,
  plant_date: '',
  expected_harvest_date: undefined,
  unit: CropUnit.KG,
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

  if (!formData.area || formData.area <= 0) {
    errors.area = '请输入有效的种植面积'
    isValid = false
  }

  if (!formData.plant_date) {
    errors.plant_date = '请选择种植日期'
    isValid = false
  }

  if (formData.expected_harvest_date && formData.plant_date) {
    if (formData.expected_harvest_date < formData.plant_date) {
      errors.expected_harvest_date = '预计收获日期不能早于种植日期'
      isValid = false
    }
  }

  return isValid
}

async function handleSubmit() {
  if (!validate()) return

  loading.value = true
  submitError.value = null

  try {
    await cropsStore.createCrop(formData)
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
