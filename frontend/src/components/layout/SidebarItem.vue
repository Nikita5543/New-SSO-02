<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { ChevronRight } from 'lucide-vue-next'
import Collapsible from '@/components/ui/Collapsible.vue'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  isSubItem: {
    type: Boolean,
    default: false,
  },
})

const route = useRoute()

const isActive = computed(() => {
  if (props.item.children && props.item.children.length) {
    return props.item.children.some((child) => route.path === child.path)
  }
  return route.path === props.item.path
})

const hasChildren = computed(() =>
  props.item.children && props.item.children.length > 0
)
</script>

<template>
  <!-- Item with children (collapsible) -->
  <Collapsible v-if="hasChildren" :default-open="isActive">
    <template #trigger="{ isOpen }">
      <div
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent"
        :class="isActive ? 'bg-accent text-accent-foreground' : 'text-muted-foreground hover:text-accent-foreground'"
      >
        <component :is="item.icon" v-if="item.icon" class="h-4 w-4 shrink-0" />
        <span class="flex-1 truncate font-medium">{{ item.label }}</span>
        <ChevronRight
          class="h-4 w-4 shrink-0 transition-transform duration-200"
          :class="{ 'rotate-90': isOpen }"
        />
      </div>
    </template>
    <div class="ml-4 mt-1 space-y-1 border-l border-border pl-3">
      <SidebarItem
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :is-sub-item="true"
      />
    </div>
  </Collapsible>

  <!-- Single item (link) -->
  <RouterLink
    v-else
    :to="item.path"
    class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent hover:text-accent-foreground"
    :class="[
      route.path === item.path
        ? 'bg-accent text-accent-foreground font-medium'
        : 'text-muted-foreground',
      isSubItem ? 'py-1.5' : ''
    ]"
  >
    <component :is="item.icon" v-if="item.icon && !isSubItem" class="h-4 w-4 shrink-0" />
    <span class="truncate font-medium">{{ item.label }}</span>
  </RouterLink>
</template>
