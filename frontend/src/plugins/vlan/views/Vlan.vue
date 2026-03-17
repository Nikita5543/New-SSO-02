<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Badge from '@/components/ui/Badge.vue'
import { 
  Network, 
  RefreshCw, 
  Search,
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  XCircle,
  Info
} from 'lucide-vue-next'

const authStore = useAuthStore()
const activeTab = ref('free')
const freeVlans = ref([])
const occupiedVlans = ref([])
const stats = ref(null)
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(100)
const totalItems = ref(0)

const tabs = [
  { id: 'free', label: 'FREE VLAN DATABASE', icon: CheckCircle2 },
  { id: 'occupied', label: 'Occupied VLANs', icon: XCircle },
]

async function fetchFreeVlans() {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      page_size: pageSize.value.toString(),
    })
    
    if (searchQuery.value) params.append('search', searchQuery.value)
    
    const response = await authStore.authFetch(`/api/v1/plugins/vlan/free-vlans?${params.toString()}`)
    
    if (response.ok) {
      const data = await response.json()
      freeVlans.value = data.results || []
      totalItems.value = data.count || 0
    }
  } catch (e) {
    console.error('Error fetching free VLANs:', e)
  } finally {
    loading.value = false
  }
}

async function fetchOccupiedVlans() {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      page_size: pageSize.value.toString(),
    })
    
    const response = await authStore.authFetch(`/api/v1/plugins/vlan/occupied-vlans?${params.toString()}`)
    
    if (response.ok) {
      const data = await response.json()
      occupiedVlans.value = data.results || []
      totalItems.value = data.count || 0
    }
  } catch (e) {
    console.error('Error fetching occupied VLANs:', e)
  } finally {
    loading.value = false
  }
}

async function fetchStats() {
  try {
    const response = await authStore.authFetch('/api/v1/plugins/vlan/vlan-stats')
    if (response.ok) {
      stats.value = await response.json()
    }
  } catch (e) {
    console.error('Error fetching stats:', e)
  }
}

function fetchData() {
  currentPage.value = 1
  if (activeTab.value === 'free') {
    fetchFreeVlans()
  } else {
    fetchOccupiedVlans()
  }
}

function switchTab(tabId) {
  activeTab.value = tabId
  searchQuery.value = ''
  currentPage.value = 1
  fetchData()
}

const currentData = computed(() => {
  return activeTab.value === 'free' ? freeVlans.value : occupiedVlans.value
})

onMounted(() => {
  fetchFreeVlans()
  fetchStats()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">VLAN Management</h1>
        <p class="text-muted-foreground mt-1">Free and occupied VLAN database</p>
      </div>
    </div>

    <!-- Stats Cards -->
    <div v-if="stats" class="grid gap-4 md:grid-cols-3">
      <Card>
        <CardContent class="p-4">
          <div class="flex items-center gap-4">
            <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Network class="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p class="text-sm text-muted-foreground">Total Unique VLANs</p>
              <p class="text-2xl font-bold">{{ stats.total_unique_vlans }}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardContent class="p-4">
          <div class="flex items-center gap-4">
            <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <CheckCircle2 class="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p class="text-sm text-muted-foreground">Free VLANs</p>
              <p class="text-2xl font-bold text-green-600">{{ stats.free_vlans }}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardContent class="p-4">
          <div class="flex items-center gap-4">
            <div class="p-2 bg-red-100 dark:bg-red-900 rounded-lg">
              <XCircle class="h-5 w-5 text-red-600 dark:text-red-400" />
            </div>
            <div>
              <p class="text-sm text-muted-foreground">Occupied VLANs</p>
              <p class="text-2xl font-bold text-red-600">{{ stats.occupied_vlans }}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Tabs -->
    <Card>
      <CardContent class="p-0">
        <div class="border-b">
          <nav class="flex" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="switchTab(tab.id)"
              :class="[
                activeTab === tab.id
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:text-foreground hover:border-muted-foreground/50',
                'flex items-center gap-2 border-b-2 px-6 py-4 text-sm font-medium transition-colors'
              ]"
            >
              <component :is="tab.icon" class="h-4 w-4" />
              {{ tab.label }}
            </button>
          </nav>
        </div>
      </CardContent>
    </Card>

    <!-- Search -->
    <Card>
      <CardContent class="p-4">
        <div class="flex flex-col gap-4 sm:flex-row">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              v-model="searchQuery"
              :placeholder="activeTab === 'free' ? 'Search by VLAN ID or previous client...' : 'Search...'"
              class="pl-9"
              @keyup.enter="fetchData"
            />
          </div>
          <Button @click="fetchData" :disabled="loading">
            <Search class="h-4 w-4 mr-2" />
            Search
          </Button>
          <Button variant="outline" @click="fetchData" :disabled="loading">
            <RefreshCw :class="['h-4 w-4 mr-2', loading ? 'animate-spin' : '']" />
            Refresh
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Free VLANs Table -->
    <Card v-if="activeTab === 'free'">
      <CardHeader>
        <CardTitle>Free VLAN Database</CardTitle>
        <CardDescription>
          VLANs that are available for use (all services with these VLANs are disabled)
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="loading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="freeVlans.length === 0" class="text-center py-12 text-muted-foreground">
          <CheckCircle2 class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold">No free VLANs found</h3>
          <p class="text-sm mt-1">All VLANs are currently in use</p>
        </div>

        <div v-else class="rounded-md border">
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b bg-muted/50">
                  <th class="px-4 py-3 text-left font-medium">VLAN ID</th>
                  <th class="px-4 py-3 text-left font-medium">Previous Services Count</th>
                  <th class="px-4 py-3 text-left font-medium">Previous Clients (Disabled)</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="vlan in freeVlans"
                  :key="vlan.vlan_id"
                  class="border-b last:border-b-0 hover:bg-muted/50"
                >
                  <td class="px-4 py-3">
                    <Badge variant="outline" class="text-lg font-mono">
                      {{ vlan.vlan_id }}
                    </Badge>
                  </td>
                  <td class="px-4 py-3">
                    <Badge variant="secondary">{{ vlan.service_count }}</Badge>
                  </td>
                  <td class="px-4 py-3">
                    <div class="space-y-1">
                      <div 
                        v-for="(service, idx) in vlan.previous_services.slice(0, 3)" 
                        :key="idx"
                        class="text-sm"
                      >
                        <span class="font-medium">{{ service.client || 'Unknown' }}</span>
                        <span class="text-muted-foreground">({{ service.activity }})</span>
                      </div>
                      <div v-if="vlan.previous_services.length > 3" class="text-sm text-muted-foreground">
                        +{{ vlan.previous_services.length - 3 }} more...
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="freeVlans.length > 0" class="flex items-center justify-between mt-4">
          <div class="text-sm text-muted-foreground">
            Page {{ currentPage }} of {{ Math.ceil(totalItems / pageSize) }}
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage--; fetchFreeVlans()"
            >
              <ChevronLeft class="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage * pageSize >= totalItems"
              @click="currentPage++; fetchFreeVlans()"
            >
              <ChevronRight class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Occupied VLANs Table -->
    <Card v-if="activeTab === 'occupied'">
      <CardHeader>
        <CardTitle>Occupied VLANs</CardTitle>
        <CardDescription>
          VLANs currently in use by active services
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="loading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="occupiedVlans.length === 0" class="text-center py-12 text-muted-foreground">
          <XCircle class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold">No occupied VLANs found</h3>
        </div>

        <div v-else class="rounded-md border">
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b bg-muted/50">
                  <th class="px-4 py-3 text-left font-medium">VLAN ID</th>
                  <th class="px-4 py-3 text-left font-medium">Active Services</th>
                  <th class="px-4 py-3 text-left font-medium">Clients</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="vlan in occupiedVlans"
                  :key="vlan.vlan_id"
                  class="border-b last:border-b-0 hover:bg-muted/50"
                >
                  <td class="px-4 py-3">
                    <Badge variant="outline" class="text-lg font-mono text-red-600">
                      {{ vlan.vlan_id }}
                    </Badge>
                  </td>
                  <td class="px-4 py-3">
                    <Badge variant="secondary">{{ vlan.service_count }}</Badge>
                  </td>
                  <td class="px-4 py-3">
                    <div class="space-y-1">
                      <div 
                        v-for="(service, idx) in vlan.services.slice(0, 3)" 
                        :key="idx"
                        class="text-sm"
                      >
                        <span class="font-medium">{{ service.client || 'Unknown' }}</span>
                        <Badge 
                          :class="service.status === 'Эксплуатация' ? 'bg-green-500' : 'bg-gray-500'"
                          class="ml-2 text-xs"
                        >
                          {{ service.status }}
                        </Badge>
                      </div>
                      <div v-if="vlan.services.length > 3" class="text-sm text-muted-foreground">
                        +{{ vlan.services.length - 3 }} more...
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="occupiedVlans.length > 0" class="flex items-center justify-between mt-4">
          <div class="text-sm text-muted-foreground">
            Page {{ currentPage }} of {{ Math.ceil(totalItems / pageSize) }}
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage--; fetchOccupiedVlans()"
            >
              <ChevronLeft class="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage * pageSize >= totalItems"
              @click="currentPage++; fetchOccupiedVlans()"
            >
              <ChevronRight class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Info Card -->
    <Card class="bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800">
      <CardContent class="p-4">
        <div class="flex items-start gap-3">
          <Info class="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
          <div>
            <h4 class="font-medium text-blue-900 dark:text-blue-100">How it works</h4>
            <p class="text-sm text-blue-700 dark:text-blue-300 mt-1">
              VLAN is considered <strong>occupied</strong> if at least one service with this VLAN has status "Эксплуатация".
              VLAN is considered <strong>free</strong> if all services with this VLAN have status "Отключен" or no services use this VLAN.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
