<script setup>
import { useThemeStore } from '@/stores/theme'
import DropdownMenu from './DropdownMenu.vue'
import DropdownMenuItem from './DropdownMenuItem.vue'
import { Sun, Moon, Monitor } from 'lucide-vue-next'

const themeStore = useThemeStore()
</script>

<template>
  <DropdownMenu>
    <template #trigger>
      <button
        class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-input bg-background text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
      >
        <Sun v-if="!themeStore.isDark" class="h-4 w-4" />
        <Moon v-else class="h-4 w-4" />
      </button>
    </template>
    <template #default="{ close }">
      <DropdownMenuItem @click="themeStore.setTheme('light'); close()">
        <Sun class="mr-2 h-4 w-4" />
        <span>Light</span>
      </DropdownMenuItem>
      <DropdownMenuItem @click="themeStore.setTheme('dark'); close()">
        <Moon class="mr-2 h-4 w-4" />
        <span>Dark</span>
      </DropdownMenuItem>
      <DropdownMenuItem @click="themeStore.setTheme('system'); close()">
        <Monitor class="mr-2 h-4 w-4" />
        <span>System</span>
      </DropdownMenuItem>
    </template>
  </DropdownMenu>
</template>
