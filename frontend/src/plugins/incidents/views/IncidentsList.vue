<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import { AlertTriangle, Plus, RefreshCw, CheckCircle2, Clock, XCircle } from 'lucide-vue-next'

const authStore = useAuthStore()
const incidents = ref([])
const loading = ref(false)
const error = ref(null)
const showCreateForm = ref(false)
const newIncident = ref({
  title: '',
  description: '',
  severity: 'minor',
  affected_system: ''
})

const severityConfig = {
  critical: { color: 'bg-red-500', text: 'text-red-500', label: 'Critical' },
  major: { color: 'bg-orange-500', text: 'text-orange-500', label: 'Major' },
  minor: { color: 'bg-yellow-500', text: 'text-yellow-500', label: 'Minor' },
  info: { color: 'bg-blue-500', text: 'text-blue-500', label: 'Info' }
}

const statusConfig = {
  open: { icon: Clock, color: 'text-blue-500', label: 'Open' },
  investigating: { icon: RefreshCw, color: 'text-yellow-500', label: 'Investigating' },
  resolved: { icon: CheckCircle2, color: 'text-green-500', label: 'Resolved' },
  closed: { icon: XCircle, color: 'text-gray-500', label: 'Closed' }
}

async function fetchIncidents() {
  loading.value = true
  error.value = null
  try {
    const response = await authStore.authFetch('/api/v1/plugins/incidents/')
    if (response.ok) {
      incidents.value = await response.json()
    }
  } catch (e) {
    error.value = 'Failed to load incidents'
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function createIncident() {
  if (!newIncident.value.title || !newIncident.value.description) {
    return
  }
  
  try {
    const response = await authStore.authFetch('/api/v1/plugins/incidents/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newIncident.value)
    })
    
    if (response.ok) {
      await fetchIncidents()
      showCreateForm.value = false
      newIncident.value = {
        title: '',
        description: '',
        severity: 'minor',
        affected_system: ''
      }
    }
  } catch (e) {
    error.value = 'Failed to create incident'
    console.error(e)
  }
}

async function updateStatus(incidentId, newStatus) {
  try {
    const response = await authStore.authFetch(`/api/v1/plugins/incidents/${incidentId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    
    if (response.ok) {
      await fetchIncidents()
    }
  } catch (e) {
    error.value = 'Failed to update incident'
    console.error(e)
  }
}

onMounted(() => {
  fetchIncidents()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Incidents</h1>
        <p class="text-muted-foreground mt-1">Manage and track network incidents</p>
      </div>
      <Button @click="showCreateForm = !showCreateForm">
        <Plus class="h-4 w-4 mr-2" />
        New Incident
      </Button>
    </div>

    <!-- Create Form -->
    <Card v-if="showCreateForm">
      <CardHeader>
        <CardTitle>Create New Incident</CardTitle>
        <CardDescription>Report a new network incident or issue</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="createIncident" class="space-y-4">
          <div>
            <Label for="title">Title</Label>
            <Input
              id="title"
              v-model="newIncident.title"
              placeholder="Brief description of the incident"
              required
            />
          </div>
          <div>
            <Label for="description">Description</Label>
            <textarea
              id="description"
              v-model="newIncident.description"
              placeholder="Detailed description of the incident"
              rows="4"
              class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              required
            ></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <Label for="severity">Severity</Label>
              <select
                id="severity"
                v-model="newIncident.severity"
                class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="info">Info</option>
                <option value="minor">Minor</option>
                <option value="major">Major</option>
                <option value="critical">Critical</option>
              </select>
            </div>
            <div>
              <Label for="affected_system">Affected System</Label>
              <Input
                id="affected_system"
                v-model="newIncident.affected_system"
                placeholder="System name or ID"
              />
            </div>
          </div>
          <div class="flex gap-2">
            <Button type="submit">Create Incident</Button>
            <Button type="button" variant="outline" @click="showCreateForm = false">Cancel</Button>
          </div>
        </form>
      </CardContent>
    </Card>

    <!-- Error Message -->
    <div v-if="error" class="rounded-lg bg-destructive/10 p-4 text-destructive">
      {{ error }}
    </div>

    <!-- Incidents List -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
    </div>

    <div v-else-if="incidents.length === 0" class="rounded-lg border border-dashed p-12 text-center">
      <AlertTriangle class="mx-auto h-12 w-12 text-muted-foreground" />
      <h3 class="mt-4 text-lg font-semibold">No incidents found</h3>
      <p class="mt-2 text-sm text-muted-foreground">
        Create a new incident to get started
      </p>
    </div>

    <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <Card v-for="incident in incidents" :key="incident.id">
        <CardHeader>
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-2">
              <div 
                :class="['h-3 w-3 rounded-full', severityConfig[incident.severity]?.color]"
              ></div>
              <CardTitle class="text-lg">{{ incident.title }}</CardTitle>
            </div>
            <Badge :variant="incident.status === 'resolved' ? 'default' : 'secondary'">
              <component 
                :is="statusConfig[incident.status]?.icon" 
                :class="['h-3 w-3 mr-1 inline', statusConfig[incident.status]?.color]"
              />
              {{ statusConfig[incident.status]?.label }}
            </Badge>
          </div>
          <CardDescription class="line-clamp-2">
            {{ incident.description }}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-muted-foreground">Severity:</span>
              <span :class="['font-medium', severityConfig[incident.severity]?.text]">
                {{ severityConfig[incident.severity]?.label }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Affected System:</span>
              <span class="font-medium">{{ incident.affected_system || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-muted-foreground">Created:</span>
              <span class="font-medium">{{ new Date(incident.created_at).toLocaleDateString() }}</span>
            </div>
          </div>
          
          <div class="mt-4 flex gap-2">
            <Button 
              v-if="incident.status === 'open'" 
              size="sm" 
              variant="outline"
              @click="updateStatus(incident.id, 'investigating')"
            >
              Investigate
            </Button>
            <Button 
              v-if="incident.status === 'investigating'" 
              size="sm"
              @click="updateStatus(incident.id, 'resolved')"
            >
              Resolve
            </Button>
            <Button 
              v-if="incident.status !== 'closed' && incident.status !== 'resolved'" 
              size="sm" 
              variant="ghost"
              @click="updateStatus(incident.id, 'closed')"
            >
              Close
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
