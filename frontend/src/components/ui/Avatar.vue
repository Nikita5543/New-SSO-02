<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  src: String,
  alt: String,
  fallback: String,
  size: {
    type: String,
    default: 'md',
  },
  class: String,
})

const sizeClasses = {
  sm: 'h-8 w-8 text-xs',
  md: 'h-10 w-10 text-sm',
  lg: 'h-12 w-12 text-base',
}

const initials = computed(() => {
  if (props.fallback) return props.fallback
  if (props.alt) {
    return props.alt
      .split(' ')
      .map((w) => w[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }
  return '?'
})
</script>

<template>
  <div
    :class="cn(
      'relative flex shrink-0 overflow-hidden rounded-full',
      sizeClasses[size],
      $props.class
    )"
  >
    <img
      v-if="src"
      :src="src"
      :alt="alt"
      class="aspect-square h-full w-full object-cover"
    />
    <div
      v-else
      class="flex h-full w-full items-center justify-center rounded-full bg-muted font-medium"
    >
      {{ initials }}
    </div>
  </div>
</template>
