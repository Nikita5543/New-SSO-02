<script setup>
import { ref, computed } from 'vue'
import { ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  defaultOpen: {
    type: Boolean,
    default: false,
  },
})

const isOpen = ref(props.defaultOpen)

function toggle() {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <div>
    <div class="cursor-pointer" @click="toggle">
      <slot name="trigger" :is-open="isOpen">
        <div class="flex items-center">
          <ChevronRight
            class="h-4 w-4 shrink-0 transition-transform duration-200"
            :class="{ 'rotate-90': isOpen }"
          />
        </div>
      </slot>
    </div>
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-96"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 max-h-96"
      leave-to-class="opacity-0 max-h-0"
    >
      <div v-show="isOpen" class="overflow-hidden">
        <slot :is-open="isOpen" />
      </div>
    </Transition>
  </div>
</template>
