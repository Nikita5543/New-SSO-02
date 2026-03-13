<script setup>
import { cn } from '@/lib/utils'

defineProps({
  class: String,
})
</script>

<template>
  <div
    :class="cn('relative overflow-auto', $props.class)"
    style="scrollbar-width: thin; scrollbar-color: hsl(var(--muted)) transparent;"
  >
    <slot />
  </div>
</template>
