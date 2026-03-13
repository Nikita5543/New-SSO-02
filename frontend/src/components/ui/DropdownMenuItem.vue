<script setup>
import { cn } from '@/lib/utils'

defineProps({
  class: String,
  disabled: Boolean,
})

const emit = defineEmits(['click'])
</script>

<template>
  <div
    :class="cn(
      'relative flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors hover:bg-accent hover:text-accent-foreground',
      disabled && 'pointer-events-none opacity-50',
      $props.class
    )"
    @click="emit('click', $event)"
  >
    <slot />
  </div>
</template>
