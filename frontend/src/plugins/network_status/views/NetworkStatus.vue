<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import { 
  Network, 
  RefreshCw, 
  Play, 
  PlayCircle,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Database,
  Calendar
} from 'lucide-vue-next'

const authStore = useAuthStore()
const devices = ref([])
const summary = ref({})
const loading = ref(false)
const syncing = ref(false)
const checking = ref({}) // Track which devices are being checked

// Fetch devices with status
async function fetchDevices(sync = false) {
  loading.value = true
  try {
    const url = `/api/v1/plugins/network_status/devices${sync ? '?sync=true' : ''}`
    const response = await authStore.authFetch(url)
    if (response.ok) {
      const data = await response.json()
      devices.value = data.devices || []
      summary.value = data.summary || {}
    }
  } catch (e) {
    console.error('Error fetching devices:', e)
  } finally {
    loading.value = false
  }
}

// Sync devices from NetBox
async function syncFromNetBox() {
  syncing.value = true
  try {
    const response = await authStore.authFetch('/api/v1/plugins/network_status/sync-from-netbox', {
      method: 'POST'
    })
    if (response.ok) {
      await fetchDevices(true)
    }
  } catch (e) {
    console.error('Error syncing:', e)
  } finally {
    syncing.value = false
  }
}

// Run check for single device
async function checkDevice(deviceId) {
  checking.value[deviceId] = true
  try {
    const response = await authStore.authFetch(`/api/v1/plugins/network_status/devices/${deviceId}/check`, {
      method: 'POST'
    })
    if (response.ok) {
      // Refresh after a delay to get results
      setTimeout(() => fetchDevices(), 2000)
    }
  } catch (e) {
    console.error('Error checking device:', e)
  } finally {
    checking.value[deviceId] = false
  }
}

// Run check for all devices
async function checkAllDevices() {
  try {
    const response = await authStore.authFetch('/api/v1/plugins/network_status/devices/check-all', {
      method: 'POST'
    })
    if (response.ok) {
      // Refresh after a delay
      setTimeout(() => fetchDevices(), 3000)
    }
  } catch (e) {
    console.error('Error checking all devices:', e)
  }
}

// Format date
function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('ru-RU')
}

// Get status color
function getStatusColor(status, type) {
  if (type === 'operational') {
    return status === 'Online' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'
  }
  if (type === 'backup' || type === 'snapshot') {
    return status === 'OK' ? 'text-green-600 bg-green-50' : 
           status === 'Failed' ? 'text-red-600 bg-red-50' : 'text-gray-600 bg-gray-50'
  }
  if (type === 'critical') {
    return status === 'YES' ? 'text-red-600 bg-red-50 font-bold' : 'text-green-600 bg-green-50'
  }
  return ''
}

// Computed summary stats
const summaryStats = computed(() => {
  const op = summary.value?.operational || {}
  const bk = summary.value?.backup || {}
  const cr = summary.value?.critical || {}
  
  return [
    { label: 'Online', value: op.online || 0, total: op.total || 0, color: 'green' },
    { label: 'Offline', value: op.offline || 0, total: op.total || 0, color: 'red' },
    { label: 'Backup OK', value: bk.ok || 0, total: bk.total || 0, color: 'blue' },
    { label: 'Critical Alarms', value: cr.yes || 0, total: cr.total || 0, color: 'red' },
  ]
})

onMounted(() => {
  fetchDevices()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Network Status</h1>
        <p class="text-muted-foreground mt-1">
          Router monitoring from NetBox
        </p>
      </div>
      <div class="flex items-center gap-2">
        <Button 
          variant="outline" 
          @click="syncFromNetBox" 
          :disabled="syncing"
          class="gap-2"
        >
          <RefreshCw :class="['h-4 w-4', syncing && 'animate-spin']" />
          Sync from NetBox
        </Button>
        <Button 
          @click="checkAllDevices" 
          :disabled="loading"
          class="gap-2"
        >
          <PlayCircle class="h-4 w-4" />
          Check All
        </Button>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid gap-4 md:grid-cols-4">
      <Card v-for="stat in summaryStats" :key="stat.label">
        <CardContent class="p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-muted-foreground">{{ stat.label }}</p>
              <p class="text-2xl font-bold mt-1">
                {{ stat.value }}
                <span class="text-sm text-muted-foreground font-normal">/ {{ stat.total }}</span>
              </p>
            </div>
            <div :class="['w-3 h-3 rounded-full', `bg-${stat.color}-500`]"></div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Devices Table -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Network class="h-5 w-5" />
          Device Status
        </CardTitle>
        <CardDescription>
          Click "Check" to run status verification
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b bg-muted/50">
                <th class="text-left p-3 font-medium">Hostname</th>
                <th class="text-left p-3 font-medium">MGMT IP</th>
                <th class="text-left p-3 font-medium">Platform</th>
                <th class="text-left p-3 font-medium">Date</th>
                <th class="text-left p-3 font-medium">Operational</th>
                <th class="text-left p-3 font-medium">Backup</th>
                <th class="text-left p-3 font-medium">Snapshot</th>
                <th class="text-left p-3 font-medium">Critical</th>
                <th class="text-left p-3 font-medium">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="item in devices" 
                :key="item.device.id"
                class="border-b hover:bg-muted/50"
              >
                <td class="p-3 font-medium">{{ item.device.hostname }}</td>
                <td class="p-3 text-muted-foreground">{{ item.device.mgmt_ip }}</td>
                <td class="p-3">{{ item.device.platform || '—' }}</td>
                <td class="p-3 text-muted-foreground">
                  {{ item.latest_check ? formatDate(item.latest_check.check_date).split(',')[0] : '—' }}
                </td>
                <td class="p-3">
                  <Badge 
                    v-if="item.latest_check?.operational_status"
                    :class="getStatusColor(item.latest_check.operational_status, 'operational')"
                  >
                    {{ item.latest_check.operational_status }}
                  </Badge>
                  <span v-else class="text-muted-foreground">—</span>
                </td>
                <td class="p-3">
                  <Badge 
                    v-if="item.latest_check?.backup_status"
                    :class="getStatusColor(item.latest_check.backup_status, 'backup')"
                  >
                    {{ item.latest_check.backup_status }}
                  </Badge>
                  <span v-else class="text-muted-foreground">—</span>
                </td>
                <td class="p-3">
                  <Badge 
                    v-if="item.latest_check?.snapshot_status"
                    :class="getStatusColor(item.latest_check.snapshot_status, 'snapshot')"
                  >
                    {{ item.latest_check.snapshot_status }}
                  </Badge>
                  <span v-else class="text-muted-foreground">—</span>
                </td>
                <td class="p-3">
                  <Badge 
                    v-if="item.latest_check?.critical_alarm"
                    :class="getStatusColor(item.latest_check.critical_alarm, 'critical')"
                  >
                    {{ item.latest_check.critical_alarm }}
                  </Badge>
                  <span v-else class="text-muted-foreground">—</span>
                </td>
                <td class="p-3">
                  <Button 
                    size="sm" 
                    variant="outline"
                    @click="checkDevice(item.device.id)"
                    :disabled="checking[item.device.id]"
                    class="gap-1"
                  >
                    <Play class="h-3 w-3" />
                    {{ checking[item.device.id] ? '...' : 'Check' }}
                  </Button>
                </td>
              </tr>
            </tbody>
            <tfoot v-if="devices.length > 0" class="bg-muted/30 font-medium">
              <tr class="border-t-2">
                <td class="p-3" colspan="4">Failed/Total</td>
                <td class="p-3">
                  {{ summaryStats[1].value }}/{{ summaryStats[1].total }}
                </td>
                <td class="p-3">
                  {{ (summary.value.backup?.total || 0) - (summary.value.backup?.ok || 0) }}/{{ summary.value.backup?.total || 0 }}
                </td>
                <td class="p-3">—</td>
                <td class="p-3">
                  {{ summaryStats[3].value }}/{{ summaryStats[3].total }}
                </td>
                <td class="p-3"></td>
              </tr>
            </tfoot>
          </table>
        </div>
        
        <div v-if="devices.length === 0" class="text-center py-12 text-muted-foreground">
          <Network class="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>No devices found. Click "Sync from NetBox" to import routers.</p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
