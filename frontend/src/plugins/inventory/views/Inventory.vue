<script setup>
import { ref, onMounted } from 'vue'
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
  Server, 
  RefreshCw, 
  Search,
  ChevronDown,
  ChevronUp
} from 'lucide-vue-next'

const authStore = useAuthStore()
const activeTab = ref('devices')
const devicesLoading = ref(false)
const devicesData = ref([])
const searchQuery = ref('')
const sortField = ref('name')
const sortDirection = ref('asc')
const currentPage = ref(1)
const itemsPerPage = ref(25)
const totalItems = ref(0)

const tabs = [
  { id: 'devices', label: 'Devices', icon: Server },
]

async function fetchDevices() {
  devicesLoading.value = true
  
  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      page_size: itemsPerPage.value.toString(),
      q: searchQuery.value,
      ordering: sortDirection.value === 'asc' ? sortField.value : `-${sortField.value}`
    })
    
    const response = await authStore.authFetch(`/api/v1/plugins/inventory/devices?${params.toString()}`)
    
    if (response.ok) {
      const data = await response.json()
      devicesData.value = data.results || []
      totalItems.value = data.count || 0
    }
  } catch (e) {
    console.error('Error fetching devices:', e)
  } finally {
    devicesLoading.value = false
  }
}

function handleSort(field) {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
  fetchDevices()
}

function getStatusColor(status) {
  const colors = {
    'active': 'bg-green-500',
    'planned': 'bg-blue-500',
    'staged': 'bg-purple-500',
    'offline': 'bg-red-500',
    'decommissioned': 'bg-gray-500'
  }
  return colors[status?.value] || 'bg-gray-500'
}

function resetFilters() {
  searchQuery.value = ''
  currentPage.value = 1
  fetchDevices()
}

onMounted(() => {
  fetchDevices()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Inventory</h1>
        <p class="text-muted-foreground mt-1">Equipment inventory management from NetBox</p>
      </div>
    </div>

    <!-- Tabs -->
    <Card>
      <CardContent class="p-0">
        <div class="border-b">
          <nav class="flex" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
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

    <!-- Devices Tab -->
    <Card v-if="activeTab === 'devices'">
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Network Devices</CardTitle>
            <CardDescription>All devices from NetBox DCIM</CardDescription>
          </div>
          <Button variant="outline" @click="fetchDevices" :disabled="devicesLoading">
            <RefreshCw :class="['h-4 w-4 mr-2', devicesLoading ? 'animate-spin' : '']" />
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <!-- Search -->
        <div class="flex flex-col gap-4 mb-6">
          <div class="flex items-center gap-2">
            <div class="relative flex-1">
              <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                v-model="searchQuery"
                placeholder="Search devices..."
                class="pl-9"
                @keyup.enter="fetchDevices"
              />
            </div>
            <Button variant="outline" @click="fetchDevices" :disabled="devicesLoading">
              <Search class="h-4 w-4" />
            </Button>
            <Button variant="ghost" @click="resetFilters">
              Reset
            </Button>
          </div>
        </div>

        <!-- Devices Table -->
        <div v-if="devicesLoading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="devicesData.length === 0" class="text-center py-12 text-muted-foreground">
          <Server class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold">No devices found</h3>
          <p class="text-sm mt-1">Add devices in NetBox to see them here</p>
        </div>

        <div v-else class="rounded-md border">
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b bg-muted/50">
                  <th 
                    class="px-4 py-3 text-left font-medium cursor-pointer hover:bg-muted/70 transition-colors"
                    @click="handleSort('name')"
                  >
                    <div class="flex items-center gap-2">
                      Name
                      <ChevronDown v-if="sortField === 'name' && sortDirection === 'asc'" class="h-4 w-4" />
                      <ChevronUp v-if="sortField === 'name' && sortDirection === 'desc'" class="h-4 w-4" />
                    </div>
                  </th>
                  <th 
                    class="px-4 py-3 text-left font-medium cursor-pointer hover:bg-muted/70 transition-colors"
                    @click="handleSort('status')"
                  >
                    <div class="flex items-center gap-2">
                      Status
                      <ChevronDown v-if="sortField === 'status' && sortDirection === 'asc'" class="h-4 w-4" />
                      <ChevronUp v-if="sortField === 'status' && sortDirection === 'desc'" class="h-4 w-4" />
                    </div>
                  </th>
                  <th class="px-4 py-3 text-left font-medium">Site</th>
                  <th class="px-4 py-3 text-left font-medium">Location</th>
                  <th class="px-4 py-3 text-left font-medium">Rack</th>
                  <th class="px-4 py-3 text-left font-medium">Role</th>
                  <th class="px-4 py-3 text-left font-medium">Type</th>
                  <th class="px-4 py-3 text-left font-medium">IP Address</th>
                  <th class="px-4 py-3 text-left font-medium">Description</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="device in devicesData"
                  :key="device.id"
                  class="border-b last:border-b-0 hover:bg-muted/50 transition-colors"
                >
                  <td class="px-4 py-3 font-medium">{{ device.name }}</td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div :class="['h-2 w-2 rounded-full', getStatusColor(device.status)]"></div>
                      {{ device.status?.label || device.status?.value }}
                    </div>
                  </td>
                  <td class="px-4 py-3">{{ device.site?.name || '—' }}</td>
                  <td class="px-4 py-3">{{ device.location?.name || '—' }}</td>
                  <td class="px-4 py-3">{{ device.rack?.name || '—' }}</td>
                  <td class="px-4 py-3">
                    <Badge v-if="device.role" variant="secondary">
                      {{ device.role.name }}
                    </Badge>
                  </td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <span class="text-muted-foreground">{{ device.device_type?.manufacturer?.name }}</span>
                      <span>{{ device.device_type?.model }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 font-mono">
                    {{ device.primary_ip4?.address || device.primary_ip?.address || '—' }}
                  </td>
                  <td class="px-4 py-3 text-muted-foreground">{{ device.description || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="devicesData.length > 0" class="flex items-center justify-between mt-4">
          <div class="text-sm text-muted-foreground">
            Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to {{ Math.min(currentPage * itemsPerPage, totalItems) }} of {{ totalItems }} entries
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage-- ; fetchDevices()"
            >
              Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage * itemsPerPage >= totalItems"
              @click="currentPage++ ; fetchDevices()"
            >
              Next
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
