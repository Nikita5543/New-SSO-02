<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { usePluginRegistryStore } from '@/stores/pluginRegistry'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Badge from '@/components/ui/Badge.vue'
import Button from '@/components/ui/Button.vue'
import { 
  Activity, Package, Server, AlertTriangle, AlertCircle, CheckCircle,
  Cpu, HardDrive, MemoryStick, Network, Container, RefreshCw
} from 'lucide-vue-next'

const pluginRegistry = usePluginRegistryStore()
const authStore = useAuthStore()

// System metrics
const systemMetrics = ref(null)
const containers = ref([])
const alarms = ref([])
const loading = ref(false)
const error = ref(null)
const lastUpdate = ref(null)

// Auto-refresh interval
let refreshInterval = null

// Computed stats for plugins
const pluginStats = computed(() => [
  { 
    label: 'Loaded Plugins', 
    value: pluginRegistry.enabledPlugins.length, 
    icon: Package, 
    color: 'text-blue-500',
    bgColor: 'bg-blue-500/10'
  },
  { 
    label: 'Active Plugins', 
    value: pluginRegistry.enabledPlugins.filter(p => p.enabled !== false).length, 
    icon: CheckCircle, 
    color: 'text-green-500',
    bgColor: 'bg-green-500/10'
  },
])

// Computed container stats
const containerStats = computed(() => {
  const running = containers.value.filter(c => c.state === 'running').length
  const stopped = containers.value.filter(c => c.state === 'stopped').length
  const total = containers.value.length
  return [
    { label: 'Running', value: running, color: 'text-green-500', bgColor: 'bg-green-500' },
    { label: 'Stopped', value: stopped, color: 'text-red-500', bgColor: 'bg-red-500' },
    { label: 'Total', value: total, color: 'text-blue-500', bgColor: 'bg-blue-500' },
  ]
})

// Alarm severity colors
const alarmColors = {
  critical: { icon: AlertCircle, color: 'text-red-500', bgColor: 'bg-red-500/10', borderColor: 'border-red-500' },
  warning: { icon: AlertTriangle, color: 'text-yellow-500', bgColor: 'bg-yellow-500/10', borderColor: 'border-yellow-500' },
}

// Fetch system data
async function fetchSystemData() {
  loading.value = true
  error.value = null
  
  try {
    const response = await authStore.authFetch('/api/v1/plugins/performance/system/overview')
    
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Session expired. Please login again.')
      }
      throw new Error(`HTTP ${response.status}`)
    }
    
    const data = await response.json()
    systemMetrics.value = data.metrics
    containers.value = data.containers
    alarms.value = data.alarms
    lastUpdate.value = new Date()
  } catch (err) {
    error.value = err.message
    console.error('Failed to fetch system data:', err)
  } finally {
    loading.value = false
  }
}

// Format bytes
function formatBytes(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Format timestamp
function formatTime(date) {
  if (!date) return '-'
  return date.toLocaleTimeString()
}

// Start auto-refresh
function startAutoRefresh() {
  refreshInterval = setInterval(fetchSystemData, 5000) // Refresh every 5 seconds
}

// Stop auto-refresh
function stopAutoRefresh() {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

onMounted(() => {
  fetchSystemData()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Performance & Monitoring</h1>
        <p class="text-muted-foreground mt-1">
          Real-time system monitoring and analytics
          <span v-if="lastUpdate" class="text-xs ml-2">
            (Updated: {{ formatTime(lastUpdate) }})
          </span>
        </p>
      </div>
      <Button 
        variant="outline" 
        :disabled="loading"
        @click="fetchSystemData"
        class="gap-2"
      >
        <RefreshCw :class="['h-4 w-4', loading && 'animate-spin']" />
        Refresh
      </Button>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div class="flex items-center gap-2 text-red-600 dark:text-red-400">
        <AlertCircle class="h-5 w-5" />
        <span class="font-medium">Failed to load system data: {{ error }}</span>
      </div>
    </div>

    <!-- Alarms Section - Always visible, no flickering -->
    <Card class="border-l-4" :class="alarms.length > 0 ? 'border-l-red-500' : 'border-l-green-500'">
      <CardHeader class="pb-3">
        <div class="flex items-center justify-between">
          <CardTitle class="flex items-center gap-2 text-lg">
            <component 
              :is="alarms.length > 0 ? AlertTriangle : CheckCircle" 
              :class="alarms.length > 0 ? 'text-red-500' : 'text-green-500'"
              class="h-5 w-5"
            />
            <span v-if="alarms.length > 0" class="text-red-600 dark:text-red-400">
              Active Alarms ({{ alarms.length }})
            </span>
            <span v-else class="text-green-600 dark:text-green-400">
              All Systems Operational
            </span>
          </CardTitle>
          <div v-if="loading" class="flex items-center gap-2 text-sm text-muted-foreground">
            <RefreshCw class="h-4 w-4 animate-spin" />
            Updating...
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <!-- Alarms List -->
        <div v-if="alarms.length > 0" class="grid gap-3">
          <div 
            v-for="alarm in alarms" 
            :key="alarm.timestamp + alarm.title"
            :class="[
              'flex items-start gap-3 p-4 rounded-lg border-l-4',
              alarmColors[alarm.level].bgColor,
              alarmColors[alarm.level].borderColor
            ]"
          >
            <component 
              :is="alarmColors[alarm.level].icon" 
              :class="['h-5 w-5 mt-0.5', alarmColors[alarm.level].color]" 
            />
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <span class="font-semibold" :class="alarmColors[alarm.level].color">
                  {{ alarm.title }}
                </span>
                <Badge :variant="alarm.level === 'critical' ? 'destructive' : 'secondary'">
                  {{ alarm.level.toUpperCase() }}
                </Badge>
              </div>
              <p class="text-sm text-muted-foreground mt-1">{{ alarm.message }}</p>
              <p class="text-xs text-muted-foreground mt-1">
                {{ new Date(alarm.timestamp).toLocaleString() }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- No Alarms State -->
        <div v-else class="flex items-center gap-3 p-4 bg-green-50/50 dark:bg-green-950/20 rounded-lg">
          <div class="p-2 bg-green-500/10 rounded-full">
            <CheckCircle class="h-6 w-6 text-green-500" />
          </div>
          <div>
            <p class="font-medium text-green-700 dark:text-green-300">No active alarms</p>
            <p class="text-sm text-muted-foreground">All monitored systems are running normally</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- System Metrics Grid -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <!-- CPU Card -->
      <Card>
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">CPU Usage</p>
              <p class="text-2xl font-bold mt-1">
                {{ systemMetrics?.cpu?.percent ?? '-' }}%
              </p>
              <p class="text-xs text-muted-foreground mt-1">
                {{ systemMetrics?.cpu?.count ?? '-' }} cores
              </p>
            </div>
            <div class="p-3 bg-blue-500/10 rounded-lg">
              <Cpu class="h-8 w-8 text-blue-500" />
            </div>
          </div>
          <!-- CPU Progress Bar -->
          <div class="mt-4">
            <div class="h-2 bg-muted rounded-full overflow-hidden">
              <div 
                :class="[
                  'h-full rounded-full transition-all duration-500',
                  (systemMetrics?.cpu?.percent || 0) > 90 ? 'bg-red-500' :
                  (systemMetrics?.cpu?.percent || 0) > 70 ? 'bg-yellow-500' : 'bg-green-500'
                ]"
                :style="{ width: `${systemMetrics?.cpu?.percent || 0}%` }"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Memory Card -->
      <Card>
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Memory Usage</p>
              <p class="text-2xl font-bold mt-1">
                {{ systemMetrics?.memory?.percent ?? '-' }}%
              </p>
              <p class="text-xs text-muted-foreground mt-1">
                {{ systemMetrics?.memory?.used_gb ?? '-' }} / {{ systemMetrics?.memory?.total_gb ?? '-' }} GB
              </p>
            </div>
            <div class="p-3 bg-purple-500/10 rounded-lg">
              <MemoryStick class="h-8 w-8 text-purple-500" />
            </div>
          </div>
          <!-- Memory Progress Bar -->
          <div class="mt-4">
            <div class="h-2 bg-muted rounded-full overflow-hidden">
              <div 
                :class="[
                  'h-full rounded-full transition-all duration-500',
                  (systemMetrics?.memory?.percent || 0) > 90 ? 'bg-red-500' :
                  (systemMetrics?.memory?.percent || 0) > 80 ? 'bg-yellow-500' : 'bg-green-500'
                ]"
                :style="{ width: `${systemMetrics?.memory?.percent || 0}%` }"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Disk Card -->
      <Card>
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Disk Usage</p>
              <p class="text-2xl font-bold mt-1">
                {{ systemMetrics?.disk?.percent ?? '-' }}%
              </p>
              <p class="text-xs text-muted-foreground mt-1">
                {{ systemMetrics?.disk?.used_gb ?? '-' }} / {{ systemMetrics?.disk?.total_gb ?? '-' }} GB
              </p>
            </div>
            <div class="p-3 bg-orange-500/10 rounded-lg">
              <HardDrive class="h-8 w-8 text-orange-500" />
            </div>
          </div>
          <!-- Disk Progress Bar -->
          <div class="mt-4">
            <div class="h-2 bg-muted rounded-full overflow-hidden">
              <div 
                :class="[
                  'h-full rounded-full transition-all duration-500',
                  (systemMetrics?.disk?.percent || 0) > 90 ? 'bg-red-500' :
                  (systemMetrics?.disk?.percent || 0) > 80 ? 'bg-yellow-500' : 'bg-green-500'
                ]"
                :style="{ width: `${systemMetrics?.disk?.percent || 0}%` }"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Network Card -->
      <Card>
        <CardContent class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">Network I/O</p>
              <p class="text-lg font-bold mt-1">
                ↓ {{ systemMetrics?.network?.bytes_recv_mb ?? '-' }} MB
              </p>
              <p class="text-lg font-bold">
                ↑ {{ systemMetrics?.network?.bytes_sent_mb ?? '-' }} MB
              </p>
            </div>
            <div class="p-3 bg-cyan-500/10 rounded-lg">
              <Network class="h-8 w-8 text-cyan-500" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Load Average -->
    <Card v-if="systemMetrics?.cpu?.load_avg_1m">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Activity class="h-5 w-5" />
          System Load Average
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-3 gap-4">
          <div class="text-center p-4 bg-muted rounded-lg">
            <p class="text-sm text-muted-foreground">1 Minute</p>
            <p class="text-2xl font-bold">{{ systemMetrics.cpu.load_avg_1m.toFixed(2) }}</p>
          </div>
          <div class="text-center p-4 bg-muted rounded-lg">
            <p class="text-sm text-muted-foreground">5 Minutes</p>
            <p class="text-2xl font-bold">{{ systemMetrics.cpu.load_avg_5m.toFixed(2) }}</p>
          </div>
          <div class="text-center p-4 bg-muted rounded-lg">
            <p class="text-sm text-muted-foreground">15 Minutes</p>
            <p class="text-2xl font-bold">{{ systemMetrics.cpu.load_avg_15m.toFixed(2) }}</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Docker Containers -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle class="flex items-center gap-2">
            <Container class="h-5 w-5" />
            Docker Containers
          </CardTitle>
          <div class="flex gap-2">
            <div 
              v-for="stat in containerStats" 
              :key="stat.label"
              class="flex items-center gap-1 text-sm"
            >
              <span :class="['w-2 h-2 rounded-full', stat.bgColor]" />
              <span class="text-muted-foreground">{{ stat.label }}:</span>
              <span :class="['font-medium', stat.color]">{{ stat.value }}</span>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div class="grid gap-3">
          <div
            v-for="container in containers"
            :key="container.name"
            class="flex items-center justify-between p-3 rounded-lg border"
            :class="container.state === 'running' ? 'bg-green-50/50 dark:bg-green-950/20' : 'bg-red-50/50 dark:bg-red-950/20'"
          >
            <div class="flex items-center gap-3">
              <div 
                class="w-3 h-3 rounded-full"
                :class="container.state === 'running' ? 'bg-green-500' : 'bg-red-500'"
              />
              <div>
                <p class="font-medium">{{ container.name }}</p>
                <p class="text-xs text-muted-foreground">{{ container.image }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <p class="text-sm text-muted-foreground">{{ container.status }}</p>
              <Badge 
                :variant="container.state === 'running' ? 'default' : 'destructive'"
              >
                {{ container.state }}
              </Badge>
            </div>
          </div>
        </div>
        <div v-if="containers.length === 0" class="text-center py-8 text-muted-foreground">
          No containers found or Docker not available
        </div>
      </CardContent>
    </Card>

    <!-- Plugins Section -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Package class="h-5 w-5" />
          Loaded Plugins
        </CardTitle>
        <CardDescription>Active system modules</CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Plugin Stats -->
        <div class="grid gap-4 md:grid-cols-2 mb-6">
          <Card v-for="stat in pluginStats" :key="stat.label">
            <CardContent class="p-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-muted-foreground">{{ stat.label }}</p>
                  <p class="text-2xl font-bold">{{ stat.value }}</p>
                </div>
                <div :class="['p-2 rounded-lg', stat.bgColor]">
                  <component :is="stat.icon" :class="['h-6 w-6', stat.color]" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Plugin List -->
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
