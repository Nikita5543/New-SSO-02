<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import { 
  ExternalLink,
  Server,
  Globe,
  Database,
  Activity,
  FileText,
  LayoutDashboard,
  Search,
  BookOpen
} from 'lucide-vue-next'

const authStore = useAuthStore()
const activeTab = ref('internal')
const internalTools = ref([])
const externalTools = ref([])
const loading = ref(false)

// Tool icon mapping
const toolIcons = {
  'NetBox': Database,
  'LibreNMS': Activity,
  'ServiceBase': Server,
  'Zabbix': Activity,
  'Wiki-NOC': FileText,
  'Jira-SPD': LayoutDashboard,
  'Grafana': LayoutDashboard,
  'LG': Search,
  'RIPE Database': Globe,
  'Whois': Search,
}

function getToolIcon(name) {
  return toolIcons[name] || ExternalLink
}

// Fetch tools
async function fetchTools() {
  loading.value = true
  try {
    const [internalRes, externalRes] = await Promise.all([
      authStore.authFetch('/api/v1/plugins/network_tools/internal-tools'),
      authStore.authFetch('/api/v1/plugins/network_tools/external-tools')
    ])
    
    if (internalRes.ok) {
      const data = await internalRes.json()
      internalTools.value = data.tools || []
    }
    
    if (externalRes.ok) {
      const data = await externalRes.json()
      externalTools.value = data.tools || []
    }
  } catch (e) {
    console.error('Error fetching tools:', e)
  } finally {
    loading.value = false
  }
}

// Open tool in new tab
function openTool(url) {
  window.open(url, '_blank', 'noopener,noreferrer')
}

onMounted(() => {
  fetchTools()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Network Tools</h1>
      <p class="text-muted-foreground mt-1">
        Quick access to internal and external network resources
      </p>
    </div>

    <!-- Tabs -->
    <div class="border-b">
      <div class="flex gap-4">
        <button
          @click="activeTab = 'internal'"
          :class="[
            'pb-3 px-1 text-sm font-medium border-b-2 transition-colors',
            activeTab === 'internal'
              ? 'border-primary text-primary'
              : 'border-transparent text-muted-foreground hover:text-foreground'
          ]"
        >
          <span class="flex items-center gap-2">
            <Server class="h-4 w-4" />
            Internal Tools Systems
          </span>
        </button>
        <button
          @click="activeTab = 'external'"
          :class="[
            'pb-3 px-1 text-sm font-medium border-b-2 transition-colors',
            activeTab === 'external'
              ? 'border-primary text-primary'
              : 'border-transparent text-muted-foreground hover:text-foreground'
          ]"
        >
          <span class="flex items-center gap-2">
            <Globe class="h-4 w-4" />
            External Tools
          </span>
        </button>
      </div>
    </div>

    <!-- Internal Tools Tab -->
    <div v-if="activeTab === 'internal'" class="space-y-4">
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <Card
          v-for="tool in internalTools"
          :key="tool.name"
          class="hover:shadow-md transition-shadow cursor-pointer group"
          @click="openTool(tool.url)"
        >
          <CardContent class="p-4">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-3">
                <div class="p-2 rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <component :is="getToolIcon(tool.name)" class="h-5 w-5" />
                </div>
                <div>
                  <h3 class="font-semibold">{{ tool.name }}</h3>
                  <p class="text-sm text-muted-foreground">{{ tool.description }}</p>
                </div>
              </div>
              <ExternalLink class="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- External Tools Tab -->
    <div v-if="activeTab === 'external'" class="space-y-4">
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <Card
          v-for="tool in externalTools"
          :key="tool.name"
          class="hover:shadow-md transition-shadow cursor-pointer group"
          @click="openTool(tool.url)"
        >
          <CardContent class="p-4">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-3">
                <div class="p-2 rounded-lg bg-secondary/50 text-secondary-foreground group-hover:bg-secondary transition-colors">
                  <component :is="getToolIcon(tool.name)" class="h-5 w-5" />
                </div>
                <div>
                  <h3 class="font-semibold">{{ tool.name }}</h3>
                  <p class="text-sm text-muted-foreground">{{ tool.description }}</p>
                </div>
              </div>
              <ExternalLink class="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
