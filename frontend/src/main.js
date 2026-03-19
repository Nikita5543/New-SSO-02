import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { usePluginRegistryStore } from './stores/pluginRegistry'
import { useThemeStore } from './stores/theme'
import * as icons from 'lucide-vue-next'

// Import styles
import './assets/css/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize plugin registry and load plugins dynamically
async function initializePlugins() {
  const pluginRegistry = usePluginRegistryStore()
  
  try {
    // Fetch plugin list from backend
    const response = await fetch('/api/v1/plugins')
    if (response.ok) {
      const plugins = await response.json()
      
      // Register each plugin
      for (const plugin of plugins) {
        if (plugin.status === 'loaded') {
          // Create plugin manifest with menu items
          const manifest = {
            name: plugin.name,
            label: plugin.name.charAt(0).toUpperCase() + plugin.name.slice(1),
            version: plugin.version,
            description: plugin.description,
            enabled: true,
            menuItems: getMenuItemsForPlugin(plugin.name) || []
          }
          
          pluginRegistry.registerPlugin(manifest)
        }
      }
      
      pluginRegistry.setInitialized()
      console.log(`Initialized ${plugins.length} plugins`)
    }
  } catch (error) {
    console.error('Failed to initialize plugins:', error)
  }
}

function getMenuItemsForPlugin(pluginName) {
  // Define menu items for each plugin type
  const menuConfig = {
    incidents: [
      {
        label: 'Incidents',
        icon: icons.AlertTriangle,
        path: '/plugins/incidents',
        section: 'operations',
        order: 10
      }
    ],
    inventory: [
      {
        label: 'Inventory',
        icon: icons.Package,
        path: '/plugins/inventory',
        section: 'operations',
        order: 20
      }
    ],
    performance: [
      {
        label: 'Performance',
        icon: icons.Activity,
        path: '/plugins/performance',
        section: 'analytics',
        order: 30
      }
    ],
    security_module: [
      {
        label: 'Security',
        icon: icons.Shield,
        path: '/plugins/security',
        section: 'security',
        order: 40
      }
    ],
    accounting: [
      {
        label: 'Accounting',
        icon: icons.DollarSign,
        path: '/plugins/accounting',
        section: 'admin',
        order: 50
      }
    ],
    configuration: [
      {
        label: 'Configuration',
        icon: icons.Settings,
        path: '/plugins/configuration',
        section: 'admin',
        order: 60
      }
    ],
    ipam: [
      {
        label: 'IPAM',
        icon: icons.Globe,
        path: '/plugins/ipam',
        section: 'operations',
        order: 25
      }
    ],
    customer_services: [
      {
        label: 'Customer Services',
        icon: icons.Briefcase,
        path: '/plugins/customer-services',
        section: 'operations',
        order: 30
      }
    ],
    vlan: [
      {
        label: 'VLAN',
        icon: icons.Network,
        path: '/plugins/vlan',
        section: 'operations',
        order: 35
      }
    ],
    network_status: [
      {
        label: 'Network Status',
        icon: icons.Activity,
        path: '/plugins/network-status',
        section: 'analytics',
        order: 35
      }
    ],
    network_tools: [
      {
        label: 'Network Tools',
        icon: icons.Wrench,
        path: '/plugins/network-tools',
        section: 'analytics',
        order: 40
      }
    ],
  }
  
  return menuConfig[pluginName] || []
}

// Initialize auth state before mounting
async function initApp() {
  const themeStore = useThemeStore()
  const authStore = useAuthStore()
  
  // Initialize theme first (apply Light mode by default)
  themeStore.initTheme()
  
  // Try to restore user session if token exists
  if (authStore.accessToken) {
    await authStore.fetchUser()
    // Restore user's background preference
    if (authStore.user?.background_image) {
      themeStore.setBackground(authStore.user.background_image)
    }
  }
  
  // Initialize plugins
  await initializePlugins()
  
  // Mount the app
  app.mount('#app')
}

initApp().catch(console.error)
