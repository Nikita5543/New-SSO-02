<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePluginRegistryStore } from '@/stores/pluginRegistry'
import SidebarItem from './SidebarItem.vue'
import ScrollArea from '@/components/ui/ScrollArea.vue'
import Separator from '@/components/ui/Separator.vue'
import {
  LayoutDashboard,
  Users,
  Settings,
  User,
  CreditCard,
  Bell,
  HelpCircle,
  AlertTriangle,
  Package,
  Activity,
  Shield,
  DollarSign,
} from 'lucide-vue-next'

const authStore = useAuthStore()
const pluginRegistry = usePluginRegistryStore()

const emit = defineEmits(['close'])

// Check if user has access to section based on role
function hasSectionAccess(section) {
  const userRole = authStore.userRole
  
  // Superuser has access to all sections
  if (userRole === 'superuser') {
    return true
  }
  
  // User role has limited access
  if (userRole === 'user') {
    const allowedSections = ['general', 'operations']
    return allowedSections.includes(section.toLowerCase())
  }
  
  return false
}

// Core menu items
const coreGeneralItems = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, order: 10 },
]

const corePageItems = computed(() => {
  const items = []
  // Only superuser can access Users management
  if (authStore.userRole === 'superuser') {
    items.push({ label: 'Users', path: '/users', icon: Users, order: 10 })
  }
  return items
})

const coreOtherItems = [
  {
    label: 'Settings',
    path: '/settings',
    icon: Settings,
    order: 10,
    children: [
      { label: 'Profile', path: '/settings/profile' },
      { label: 'Account', path: '/settings/account' },
      { label: 'Notifications', path: '/settings/notifications' },
      { label: 'Display', path: '/settings/display' },
    ],
  },
  { label: 'Help', path: '/help', icon: HelpCircle, order: 20 },
]

// Plugin sections
const operationsPluginItems = computed(() => 
  pluginRegistry.menuItemsBySection('operations')
)

const analyticsPluginItems = computed(() => 
  pluginRegistry.menuItemsBySection('analytics')
)

const securityPluginItems = computed(() => 
  pluginRegistry.menuItemsBySection('security')
)

const adminPluginItems = computed(() => 
  pluginRegistry.menuItemsBySection('admin')
)

// Merge core + plugin items per section
const generalItems = computed(() => {
  const pluginItems = pluginRegistry.menuItemsBySection('general')
  return [...coreGeneralItems, ...pluginItems].sort(
    (a, b) => (a.order || 0) - (b.order || 0)
  )
})

const pageItems = computed(() => {
  const pluginItems = pluginRegistry.menuItemsBySection('pages')
  return [...corePageItems.value, ...pluginItems].sort(
    (a, b) => (a.order || 0) - (b.order || 0)
  )
})

const otherItems = computed(() => {
  const pluginItems = pluginRegistry.menuItemsBySection('other')
  return [...coreOtherItems, ...pluginItems].sort(
    (a, b) => (a.order || 0) - (b.order || 0)
  )
})

function isItemVisible(item) {
  if (!item.requiredRole) return true
  return authStore.hasRole(item.requiredRole)
}
</script>

<template>
  <div class="flex h-full flex-col">
    <!-- Logo -->
    <div class="flex h-14 items-center border-b px-4">
      <RouterLink to="/dashboard" class="flex items-center gap-2" @click="emit('close')">
        <img src="/logo.png" alt="NOC Vision" class="h-8 w-8 object-contain" />
        <span class="text-lg font-semibold">NOC Vision</span>
      </RouterLink>
    </div>

    <!-- Navigation -->
    <ScrollArea class="flex-1 px-3 py-4">
      <!-- General section -->
      <div class="mb-4">
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          General
        </h4>
        <div class="space-y-1">
          <template v-for="item in generalItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>

      <Separator class="mb-4" />

      <!-- Operations section -->
      <div v-if="hasSectionAccess('operations') && operationsPluginItems.length > 0" class="mb-4">
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Operations
        </h4>
        <div class="space-y-1">
          <template v-for="item in operationsPluginItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>

      <Separator v-if="hasSectionAccess('operations') && operationsPluginItems.length > 0" class="mb-4" />

      <!-- Analytics section -->
      <div v-if="hasSectionAccess('analytics') && analyticsPluginItems.length > 0" class="mb-4">
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Analytics
        </h4>
        <div class="space-y-1">
          <template v-for="item in analyticsPluginItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>

      <Separator v-if="hasSectionAccess('analytics') && analyticsPluginItems.length > 0" class="mb-4" />

      <!-- Security section -->
      <div v-if="hasSectionAccess('security') && securityPluginItems.length > 0" class="mb-4">
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Security
        </h4>
        <div class="space-y-1">
          <template v-for="item in securityPluginItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>

      <Separator v-if="hasSectionAccess('security') && securityPluginItems.length > 0" class="mb-4" />

      <!-- Admin section -->
      <div v-if="hasSectionAccess('admin') && adminPluginItems.length > 0" class="mb-4">
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Admin
        </h4>
        <div class="space-y-1">
          <template v-for="item in adminPluginItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>

      <Separator v-if="hasSectionAccess('admin') && adminPluginItems.length > 0" class="mb-4" />

      <!-- Pages section -->
      <div v-if="pageItems.length > 0" class="mb-4">
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Pages
        </h4>
        <div class="space-y-1">
          <template v-for="item in pageItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>

      <Separator v-if="pageItems.length > 0" class="mb-4" />

      <!-- Other section -->
      <div>
        <h4 class="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Other
        </h4>
        <div class="space-y-1">
          <template v-for="item in otherItems" :key="item.path">
            <SidebarItem
              v-if="isItemVisible(item)"
              :item="item"
              @click="emit('close')"
            />
          </template>
        </div>
      </div>
    </ScrollArea>

    <!-- User info -->
    <div class="border-t p-4">
      <div class="flex items-center gap-3">
        <!-- Avatar -->
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-sm font-medium overflow-hidden">
          <img 
            v-if="authStore.user?.avatar_url && authStore.user.avatar_url.startsWith('system:')"
            :src="`/avatars/avatar-${authStore.user.avatar_url.split(':')[1]}.svg`"
            alt="Avatar"
            class="h-full w-full object-cover"
          />
          <img 
            v-else-if="authStore.user?.avatar_url"
            :src="authStore.user.avatar_url"
            alt="Avatar"
            class="h-full w-full object-cover"
          />
          <template v-else>
            {{ (authStore.user?.full_name || authStore.user?.username || '?').charAt(0).toUpperCase() }}
          </template>
        </div>
        <div class="flex-1 truncate">
          <p class="text-sm font-medium truncate">
            {{ authStore.user?.full_name || authStore.user?.username }}
          </p>
          <p class="text-xs text-muted-foreground truncate">
            {{ authStore.user?.email }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
