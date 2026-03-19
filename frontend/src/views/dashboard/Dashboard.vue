<script setup>
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Shield, Clock } from 'lucide-vue-next'

const authStore = useAuthStore()

const currentTime = new Date().toLocaleString('ru-RU', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  hour: '2-digit',
  minute: '2-digit'
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">
        Welcome back, {{ authStore.user?.full_name || authStore.user?.username }}
      </h1>
      <p class="text-muted-foreground mt-1">
        NOC Vision - Network Operations Center Platform
      </p>
    </div>

    <div class="grid gap-4 md:grid-cols-2">
      <Card>
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Your Role</p>
              <p class="text-2xl font-bold mt-1 capitalize">{{ authStore.userRole }}</p>
            </div>
            <Shield class="h-8 w-8 text-green-500" />
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Current Time</p>
              <p class="text-lg font-semibold mt-1">{{ currentTime }}</p>
            </div>
            <Clock class="h-8 w-8 text-blue-500" />
          </div>
        </CardContent>
      </Card>
    </div>

    <Card class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20">
      <CardContent class="p-6">
        <h2 class="text-lg font-semibold mb-2">Quick Navigation</h2>
        <p class="text-muted-foreground text-sm">
          Use the sidebar to navigate through plugins. Visit 
          <strong>Analytics → Performance</strong> for system monitoring and plugin status.
        </p>
      </CardContent>
    </Card>
  </div>
</template>
