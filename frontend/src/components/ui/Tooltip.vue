<script setup>
import { ref } from 'vue'

defineProps({
  text: String,
  position: {
    type: String,
    default: 'top',
  },
})

const show = ref(false)

const positionClasses = {
  top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
  bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
  left: 'right-full top-1/2 -translate-y-1/2 mr-2',
  right: 'left-full top-1/2 -translate-y-1/2 ml-2',
}
</script>

<template>
  <div
    class="relative inline-flex"
    @mouseenter="show = true"
    @mouseleave="show = false"
  >
    <slot />
    <Transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show && text"
        :class="[
          'absolute z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md whitespace-nowrap',
          positionClasses[position],
        ]"
      >
        {{ text }}
      </div>
    </Transition>
  </div>
</template>
