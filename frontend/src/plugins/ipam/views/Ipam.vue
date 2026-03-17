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
  RefreshCw, 
  Upload, 
  CheckCircle2, 
  AlertTriangle, 
  Plus, 
  Minus,
  Search,
  ChevronDown,
  ChevronUp
} from 'lucide-vue-next'

const authStore = useAuthStore()
const activeTab = ref('validation')
const validationLoading = ref(false)
const applyLoading = ref(false)
const validationResults = ref([])
const error = ref(null)

// Database state
const databaseLoading = ref(false)
const databaseData = ref([])
const searchQuery = ref('')
const sortField = ref('address')
const sortDirection = ref('asc')
const currentPage = ref(1)
const itemsPerPage = ref(25)
const totalItems = ref(0)

// Filters
const filters = ref({
  vrf: '',
  status: '',
  vlan: ''
})

const tabs = [
  { id: 'validation', label: 'Validation', icon: RefreshCw },
  { id: 'database', label: 'Database', icon: Search }
]

async function runValidation() {
  validationLoading.value = true
  error.value = null
  
  try {
    const response = await authStore.authFetch('/api/v1/plugins/ipam/validate', {
      method: 'POST'
    })
    
    if (response.ok) {
      const data = await response.json()
      // Ожидаем формат: { added: [...], removed: [...] }
      validationResults.value = transformValidationData(data)
    } else {
      error.value = 'Failed to run validation'
    }
  } catch (e) {
    error.value = 'Error running validation: ' + e.message
    console.error(e)
  } finally {
    validationLoading.value = false
  }
}

async function applyChanges() {
  applyLoading.value = true
  error.value = null
  
  try {
    const response = await authStore.authFetch('/api/v1/plugins/ipam/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ changes: validationResults.value })
    })
    
    if (response.ok) {
      alert('Changes applied successfully!')
      validationResults.value = []
    } else {
      error.value = 'Failed to apply changes'
    }
  } catch (e) {
    error.value = 'Error applying changes: ' + e.message
    console.error(e)
  } finally {
    applyLoading.value = false
  }
}

function transformValidationData(data) {
  const results = []
  
  // Transform added items
  if (data.added && Array.isArray(data.added)) {
    data.added.forEach(item => {
      results.push({
        type: 'added',
        interface: item.interface || '',
        device: item.device || '',
        ip: item.ip || '',
        description: item.description || ''
      })
    })
  }
  
  // Transform removed items
  if (data.removed && Array.isArray(data.removed)) {
    data.removed.forEach(item => {
      results.push({
        type: 'removed',
        interface: item.interface || '',
        device: item.device || '',
        ip: item.ip || '',
        description: item.description || ''
      })
    })
  }
  
  return results
}

async function fetchDatabaseData() {
  databaseLoading.value = true
  error.value = null
  
  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      page_size: itemsPerPage.value.toString(),
      q: searchQuery.value,
      ordering: sortDirection.value === 'asc' ? sortField.value : `-${sortField.value}`
    })
    
    if (filters.value.vrf) params.append('vrf_id', filters.value.vrf)
    if (filters.value.status) params.append('status', filters.value.status)
    if (filters.value.vlan) params.append('vlan_vid', filters.value.vlan)
    
    const response = await authStore.authFetch(`/api/v1/plugins/ipam/database?${params.toString()}`)
    
    if (response.ok) {
      const data = await response.json()
      databaseData.value = data.results || []
      totalItems.value = data.count || 0
    } else {
      error.value = 'Failed to load database'
    }
  } catch (e) {
    error.value = 'Error loading database: ' + e.message
    console.error(e)
  } finally {
    databaseLoading.value = false
  }
}

function handleSort(field) {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
  fetchDatabaseData()
}

function getStatusColor(status) {
  const colors = {
    'active': 'bg-green-500',
    'reserved': 'bg-blue-500',
    'deprecated': 'bg-orange-500',
    'dhcp': 'bg-purple-500'
  }
  return colors[status?.value] || 'bg-gray-500'
}

function getRowClass(type) {
  if (type === 'added') return 'bg-green-50 hover:bg-green-100 dark:bg-green-900/20 dark:hover:bg-green-900/30'
  if (type === 'removed') return 'bg-red-50 hover:bg-red-100 dark:bg-red-900/20 dark:hover:bg-red-900/30'
  return ''
}

function resetFilters() {
  searchQuery.value = ''
  filters.value = { vrf: '', status: '', vlan: '' }
  currentPage.value = 1
  fetchDatabaseData()
}

onMounted(() => {
  fetchDatabaseData()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">IPAM</h1>
        <p class="text-muted-foreground mt-1">NetBox IP Address Management integration</p>
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

    <!-- Error Message -->
    <div v-if="error" class="rounded-lg bg-destructive/10 p-4 text-destructive">
      {{ error }}
    </div>

    <!-- Validation Tab -->
    <Card v-if="activeTab === 'validation'">
      <CardHeader>
        <CardTitle>Validation</CardTitle>
        <CardDescription>Compare NetBox data with actual network state</CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Action Buttons -->
        <div class="flex gap-3 mb-6">
          <Button @click="runValidation" :disabled="validationLoading">
            <RefreshCw :class="['h-4 w-4 mr-2', validationLoading ? 'animate-spin' : '']" />
            Validation
          </Button>
          <Button 
            @click="applyChanges" 
            :disabled="applyLoading || validationResults.length === 0"
            variant="default"
          >
            <Upload :class="['h-4 w-4 mr-2', applyLoading ? 'animate-spin' : '']" />
            Apply
          </Button>
          <Badge v-if="validationResults.length > 0" variant="secondary">
            {{ validationResults.length }} changes detected
          </Badge>
        </div>

        <!-- Results Table -->
        <div v-if="validationResults.length > 0" class="rounded-md border">
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b bg-muted/50">
                  <th class="px-4 py-3 text-left font-medium">Type</th>
                  <th class="px-4 py-3 text-left font-medium">Interface</th>
                  <th class="px-4 py-3 text-left font-medium">Device</th>
                  <th class="px-4 py-3 text-left font-medium">IP Address</th>
                  <th class="px-4 py-3 text-left font-medium">Description</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, index) in validationResults"
                  :key="index"
                  :class="['border-b last:border-b-0 transition-colors', getRowClass(item.type)]"
                >
                  <td class="px-4 py-3">
                    <Badge :variant="item.type === 'added' ? 'default' : 'destructive'">
                      <component 
                        :is="item.type === 'added' ? Plus : Minus" 
                        class="h-3 w-3 mr-1 inline"
                      />
                      {{ item.type === 'added' ? 'Added' : 'Removed' }}
                    </Badge>
                  </td>
                  <td class="px-4 py-3 font-medium">{{ item.interface }}</td>
                  <td class="px-4 py-3">{{ item.device }}</td>
                  <td class="px-4 py-3 font-mono">{{ item.ip }}</td>
                  <td class="px-4 py-3 text-muted-foreground">{{ item.description }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-else-if="!validationLoading"
          class="flex flex-col items-center justify-center py-12 text-center"
        >
          <AlertTriangle class="h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold">No validation results</h3>
          <p class="text-sm text-muted-foreground mt-1">
            Click "Validation" button to compare NetBox data with network state
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="validationLoading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      </CardContent>
    </Card>

    <!-- Database Tab -->
    <Card v-else-if="activeTab === 'database'">
      <CardHeader>
        <CardTitle>IP Addresses Database</CardTitle>
        <CardDescription>All IP addresses from NetBox</CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Search and Filters -->
        <div class="flex flex-col gap-4 mb-6">
          <div class="flex items-center gap-2">
            <div class="relative flex-1">
              <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                v-model="searchQuery"
                placeholder="Search across all fields..."
                class="pl-9"
                @keyup.enter="fetchDatabaseData"
              />
            </div>
            <Button variant="outline" @click="fetchDatabaseData">
              <Search class="h-4 w-4" />
            </Button>
            <Button variant="ghost" @click="resetFilters">
              Reset
            </Button>
          </div>
          
          <!-- Advanced Filters -->
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="text-xs font-medium mb-1 block">VRF</label>
              <Input v-model="filters.vrf" placeholder="Filter by VRF" />
            </div>
            <div>
              <label class="text-xs font-medium mb-1 block">Status</label>
              <Input v-model="filters.status" placeholder="Filter by status" />
            </div>
            <div>
              <label class="text-xs font-medium mb-1 block">VLAN</label>
              <Input v-model="filters.vlan" placeholder="Filter by VLAN" />
            </div>
          </div>
        </div>

        <!-- Database Table -->
        <div v-if="databaseLoading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="databaseData.length === 0" class="text-center py-12 text-muted-foreground">
          No data found
        </div>

        <div v-else class="rounded-md border">
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b bg-muted/50">
                  <th 
                    class="px-4 py-3 text-left font-medium cursor-pointer hover:bg-muted/70 transition-colors"
                    @click="handleSort('address')"
                  >
                    <div class="flex items-center gap-2">
                      IP Address
                      <ChevronDown v-if="sortField === 'address' && sortDirection === 'asc'" class="h-4 w-4" />
                      <ChevronUp v-if="sortField === 'address' && sortDirection === 'desc'" class="h-4 w-4" />
                    </div>
                  </th>
                  <th 
                    class="px-4 py-3 text-left font-medium cursor-pointer hover:bg-muted/70 transition-colors"
                    @click="handleSort('vrf')"
                  >
                    <div class="flex items-center gap-2">
                      VRF
                      <ChevronDown v-if="sortField === 'vrf' && sortDirection === 'asc'" class="h-4 w-4" />
                      <ChevronUp v-if="sortField === 'vrf' && sortDirection === 'desc'" class="h-4 w-4" />
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
                  <th 
                    class="px-4 py-3 text-left font-medium cursor-pointer hover:bg-muted/70 transition-colors"
                    @click="handleSort('vlan')"
                  >
                    <div class="flex items-center gap-2">
                      VLAN
                      <ChevronDown v-if="sortField === 'vlan' && sortDirection === 'asc'" class="h-4 w-4" />
                      <ChevronUp v-if="sortField === 'vlan' && sortDirection === 'desc'" class="h-4 w-4" />
                    </div>
                  </th>
                  <th class="px-4 py-3 text-left font-medium">Description</th>
                  <th 
                    class="px-4 py-3 text-left font-medium cursor-pointer hover:bg-muted/70 transition-colors"
                    @click="handleSort('interface')"
                  >
                    <div class="flex items-center gap-2">
                      Interface
                      <ChevronDown v-if="sortField === 'interface' && sortDirection === 'asc'" class="h-4 w-4" />
                      <ChevronUp v-if="sortField === 'interface' && sortDirection === 'desc'" class="h-4 w-4" />
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in databaseData"
                  :key="item.id"
                  class="border-b last:border-b-0 hover:bg-muted/50 transition-colors"
                >
                  <td class="px-4 py-3 font-mono">{{ item.address }}</td>
                  <td class="px-4 py-3">{{ item.vrf?.name || 'Global' }}</td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div :class="['h-2 w-2 rounded-full', getStatusColor(item.status)]"></div>
                      {{ item.status?.label || item.status?.value }}
                    </div>
                  </td>
                  <td class="px-4 py-3">{{ item.vlan?.vid || 'N/A' }}</td>
                  <td class="px-4 py-3 text-muted-foreground">{{ item.description }}</td>
                  <td class="px-4 py-3">{{ item.interface?.name || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="databaseData.length > 0" class="flex items-center justify-between mt-4">
          <div class="text-sm text-muted-foreground">
            Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to {{ Math.min(currentPage * itemsPerPage, totalItems) }} of {{ totalItems }} entries
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage-- ; fetchDatabaseData()"
            >
              Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage * itemsPerPage >= totalItems"
              @click="currentPage++ ; fetchDatabaseData()"
            >
              Next
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
