<script setup>
import { useThemeStore } from '@/stores/theme'
import Button from '@/components/ui/Button.vue'

const themeStore = useThemeStore()
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-2xl font-bold">Display</h2>
    <div class="flex items-center justify-between">
      <div>
        <p class="font-medium">Dark Mode</p>
        <p class="text-sm text-muted-foreground">Toggle dark theme</p>
      </div>
      <Button variant="outline" @click="themeStore.toggle()">
        Toggle Theme
      </Button>
    </div>
  </div>
</template>
