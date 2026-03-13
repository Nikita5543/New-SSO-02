<script setup>
import { ref } from 'vue'
import { onClickOutside } from '@vueuse/core'

defineProps({
  class: String,
})

const open = ref(false)
const dropdownRef = ref(null)

onClickOutside(dropdownRef, () => {
  open.value = false
})

function toggle() {
  open.value = !open.value
}

function close() {
  open.value = false
}

defineExpose({ open, toggle, close })
</script>

<template>
  <div ref="dropdownRef" class="relative inline-block" :class="$props.class">
    <div @click="toggle">
      <slot name="trigger" />
    </div>
    <Transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div
        v-if="open"
        class="absolute right-0 z-50 mt-2 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md"
      >
        <slot :close="close" />
      </div>
    </Transition>
  </div>
</template>
