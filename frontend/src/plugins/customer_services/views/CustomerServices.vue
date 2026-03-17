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
  Briefcase, 
  RefreshCw, 
  Search,
  ChevronLeft,
  ChevronRight,
  Edit,
  X
} from 'lucide-vue-next'

const authStore = useAuthStore()
const services = ref([])
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(50)
const totalItems = ref(0)
const selectedService = ref(null)
const isModalOpen = ref(false)
const isEditing = ref(false)
const editForm = ref({})

// Table columns (subset for display)
const displayColumns = [
  { key: 'base_id', label: 'ID', width: '80px' },
  { key: 'activity', label: 'Activity', width: '120px' },
  { key: 'client', label: 'Client', width: '200px' },
  { key: 'type_of_service', label: 'Service Type', width: '180px' },
  { key: 'status', label: 'Status', width: '120px' },
  { key: 'speed', label: 'Speed', width: '100px' },
  { key: 'first_point', label: 'Point A', width: '250px' },
  { key: 'second_point', label: 'Point B', width: '250px' },
]

// All fields for modal
const allFields = [
  { key: 'base_id', label: 'Base ID' },
  { key: 'activity', label: 'Activity' },
  { key: 'client', label: 'Client' },
  { key: 'contract', label: 'Contract' },
  { key: 'type_of_service', label: 'Type of Service' },
  { key: 'status', label: 'Status' },
  { key: 'order_num', label: 'Order Number' },
  { key: 'first_point', label: 'First Point' },
  { key: 'second_point', label: 'Second Point' },
  { key: 'speed', label: 'Speed' },
  { key: 'vlan_id', label: 'VLAN ID' },
  { key: 'switchboard_first_point', label: 'Switchboard A' },
  { key: 'switch_port_first_point', label: 'Switch Port A' },
  { key: 'port_settings_first_point', label: 'Port Settings A' },
  { key: 'switchboard_second_point', label: 'Switchboard B' },
  { key: 'switch_port_second_point', label: 'Switch Port B' },
  { key: 'port_settings_second_point', label: 'Port Settings B' },
  { key: 'subnets', label: 'Subnets' },
  { key: 'router', label: 'Router' },
  { key: 'interface', label: 'Interface' },
  { key: 'auto_network', label: 'Auto Network' },
  { key: 'end_client', label: 'End Client' },
  { key: 'last_mile', label: 'Last Mile' },
  { key: 'id_servicepipe', label: 'ServicePipe ID' },
  { key: 'comment', label: 'Comment', type: 'textarea' },
  { key: 'responsible_department', label: 'Responsible Department' },
]

async function fetchServices() {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      page_size: pageSize.value.toString(),
    })
    
    if (searchQuery.value) params.append('search', searchQuery.value)
    if (statusFilter.value) params.append('status', statusFilter.value)
    
    const response = await authStore.authFetch(`/api/v1/plugins/customer_services/services?${params.toString()}`)
    
    if (response.ok) {
      const data = await response.json()
      services.value = data.results || []
      totalItems.value = data.count || 0
    }
  } catch (e) {
    console.error('Error fetching services:', e)
  } finally {
    loading.value = false
  }
}

function openServiceModal(service) {
  selectedService.value = service
  editForm.value = { ...service }
  isModalOpen.value = true
  isEditing.value = false
}

function closeModal() {
  isModalOpen.value = false
  selectedService.value = null
  isEditing.value = false
}

function startEditing() {
  isEditing.value = true
}

function cancelEditing() {
  editForm.value = { ...selectedService.value }
  isEditing.value = false
}

async function saveChanges() {
  try {
    const response = await authStore.authFetch(`/api/v1/plugins/customer_services/services/${selectedService.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm.value)
    })
    
    if (response.ok) {
      const updated = await response.json()
      selectedService.value = updated
      isEditing.value = false
      // Refresh list
      fetchServices()
    }
  } catch (e) {
    console.error('Error saving service:', e)
  }
}

function getStatusColor(status) {
  const colors = {
    'Эксплуатация': 'bg-green-500',
    'Отключен': 'bg-red-500',
    'Планирование': 'bg-blue-500',
  }
  return colors[status] || 'bg-gray-500'
}

function formatValue(value) {
  if (!value) return '—'
  if (typeof value === 'string' && value.length > 100) {
    return value.substring(0, 100) + '...'
  }
  return value
}

onMounted(() => {
  fetchServices()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Customer Services</h1>
        <p class="text-muted-foreground mt-1">Service database management</p>
      </div>
      <Button variant="outline" @click="fetchServices" :disabled="loading">
        <RefreshCw :class="['h-4 w-4 mr-2', loading ? 'animate-spin' : '']" />
        Refresh
      </Button>
    </div>

    <!-- Filters -->
    <Card>
      <CardContent class="p-4">
        <div class="flex flex-col gap-4 sm:flex-row">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              v-model="searchQuery"
              placeholder="Search by client, activity, ID..."
              class="pl-9"
              @keyup.enter="fetchServices"
            />
          </div>
          <Input
            v-model="statusFilter"
            placeholder="Filter by status"
            class="w-full sm:w-48"
            @keyup.enter="fetchServices"
          />
          <Button @click="fetchServices" :disabled="loading">
            <Search class="h-4 w-4 mr-2" />
            Search
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Services Table -->
    <Card>
      <CardHeader>
        <CardTitle>Services List</CardTitle>
        <CardDescription>
          Showing {{ services.length }} of {{ totalItems }} services
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="loading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="services.length === 0" class="text-center py-12 text-muted-foreground">
          <Briefcase class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold">No services found</h3>
          <p class="text-sm mt-1">Try adjusting your search criteria</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b bg-muted/50">
                <th 
                  v-for="col in displayColumns" 
                  :key="col.key"
                  class="px-3 py-3 text-left font-medium whitespace-nowrap"
                  :style="{ minWidth: col.width }"
                >
                  {{ col.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="service in services"
                :key="service.id"
                :class="[
                  'border-b last:border-b-0 cursor-pointer transition-colors',
                  service.status === 'Отключен' ? 'bg-red-50 dark:bg-red-950/20 hover:bg-red-100 dark:hover:bg-red-950/30' : 'hover:bg-muted/50'
                ]"
                @click="openServiceModal(service)"
              >
                <td 
                  v-for="col in displayColumns" 
                  :key="col.key"
                  class="px-3 py-3"
                >
                  <template v-if="col.key === 'status'">
                    <div class="flex items-center gap-2">
                      <div :class="['h-2 w-2 rounded-full', getStatusColor(service[col.key])]"></div>
                      {{ service[col.key] || '—' }}
                    </div>
                  </template>
                  <template v-else>
                    <span class="line-clamp-2">{{ formatValue(service[col.key]) }}</span>
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="services.length > 0" class="flex items-center justify-between mt-4">
          <div class="text-sm text-muted-foreground">
            Page {{ currentPage }} of {{ Math.ceil(totalItems / pageSize) }}
          </div>
          <div class="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage--; fetchServices()"
            >
              <ChevronLeft class="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              :disabled="currentPage * pageSize >= totalItems"
              @click="currentPage++; fetchServices()"
            >
              <ChevronRight class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Service Detail Modal -->
    <div 
      v-if="isModalOpen" 
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-background rounded-lg shadow-lg w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        <!-- Modal Header -->
        <div class="flex items-center justify-between border-b p-4">
          <div>
            <h2 class="text-xl font-semibold">Service Card</h2>
            <p class="text-sm text-muted-foreground">ID: {{ selectedService?.base_id }}</p>
          </div>
          <div class="flex items-center gap-2">
            <Button 
              v-if="!isEditing" 
              variant="outline" 
              size="sm"
              @click="startEditing"
            >
              <Edit class="h-4 w-4 mr-2" />
              Edit
            </Button>
            <Button variant="ghost" size="sm" @click="closeModal">
              <X class="h-4 w-4" />
            </Button>
          </div>
        </div>

        <!-- Modal Content -->
        <div class="flex-1 overflow-y-auto p-4">
          <div class="grid gap-4 md:grid-cols-2">
            <div 
              v-for="field in allFields" 
              :key="field.key"
              class="space-y-1"
              :class="field.type === 'textarea' ? 'md:col-span-2' : ''"
            >
              <label class="text-sm font-medium text-muted-foreground">{{ field.label }}</label>
              
              <!-- View Mode -->
              <div v-if="!isEditing" class="text-sm p-2 bg-muted/50 rounded">
                <template v-if="field.type === 'textarea'">
                  <pre class="whitespace-pre-wrap font-sans">{{ selectedService?.[field.key] || '—' }}</pre>
                </template>
                <template v-else>
                  {{ selectedService?.[field.key] || '—' }}
                </template>
              </div>
              
              <!-- Edit Mode -->
              <template v-else>
                <textarea
                  v-if="field.type === 'textarea'"
                  v-model="editForm[field.key]"
                  class="w-full min-h-[100px] p-2 text-sm border rounded-md bg-background"
                  rows="3"
                ></textarea>
                <input
                  v-else
                  v-model="editForm[field.key]"
                  type="text"
                  class="w-full p-2 text-sm border rounded-md bg-background"
                />
              </template>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div v-if="isEditing" class="flex items-center justify-end gap-2 border-t p-4">
          <Button variant="outline" @click="cancelEditing">Cancel</Button>
          <Button @click="saveChanges">Save Changes</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
