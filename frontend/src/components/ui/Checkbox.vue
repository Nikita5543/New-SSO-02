<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  modelValue: Boolean,
  disabled: Boolean,
  class: String,
})

const emit = defineEmits(['update:modelValue'])

const toggle = () => {
  if (!props.disabled) {
    emit('update:modelValue', !props.modelValue)
  }
}
</script>

<template>
  <button
    type="button"
    role="checkbox"
    :aria-checked="modelValue"
    :disabled="disabled"
    :class="cn(
      'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
      modelValue && 'bg-primary text-primary-foreground',
      $props.class
    )"
    @click="toggle"
  >
    <svg
      v-if="modelValue"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="3"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="h-3 w-3 mx-auto"
    >
      <polyline points="20 6 9 17 4 12" />
    </svg>
  </button>
</template>
