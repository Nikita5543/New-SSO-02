<script setup>
import { useAuthStore } from '@/stores/auth'
import { usePluginRegistryStore } from '@/stores/pluginRegistry'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Badge from '@/components/ui/Badge.vue'
import { Package, Shield } from 'lucide-vue-next'

const authStore = useAuthStore()
const pluginRegistry = usePluginRegistryStore()

const quickStats = [
  { label: 'Active Plugins', value: pluginRegistry.enabledPlugins.length, icon: Package, color: 'text-blue-500' },
  { label: 'Your Role', value: authStore.userRole, icon: Shield, color: 'text-green-500' },
]
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

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card v-for="stat in quickStats" :key="stat.label">
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">{{ stat.label }}</p>
              <p class="text-2xl font-bold mt-1">{{ stat.value }}</p>
            </div>
            <component :is="stat.icon" :class="['h-8 w-8', stat.color]" />
          </div>
        </CardContent>
      </Card>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="text-xl">Loaded Plugins</CardTitle>
        <CardDescription>Active system modules</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="plugin in pluginRegistry.enabledPlugins"
            :key="plugin.name"
            class="flex items-center gap-3 rounded-lg border p-3"
          >
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
              <Package class="h-5 w-5 text-muted-foreground" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium">{{ plugin.label }}</p>
              <p class="text-xs text-muted-foreground">v{{ plugin.version || '1.0.0' }}</p>
            </div>
            <Badge variant="secondary">Active</Badge>
          </div>
        </div>
        <div v-if="pluginRegistry.enabledPlugins.length === 0" class="text-center py-8 text-muted-foreground">
          No plugins loaded
        </div>
      </CardContent>
    </Card>
  </div>
</template>
