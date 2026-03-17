import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Core views
import SignIn from '@/views/auth/SignIn.vue'
import SignUp from '@/views/auth/SignUp.vue'
import ForgotPassword from '@/views/auth/ForgotPassword.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import NotFound from '@/views/errors/NotFound.vue'

// Settings views
import Settings from '@/views/settings/Settings.vue'
import Profile from '@/views/settings/Profile.vue'
import Account from '@/views/settings/Account.vue'
import Notifications from '@/views/settings/Notifications.vue'
import Display from '@/views/settings/Display.vue'

// Users view
import Users from '@/views/users/Users.vue'

// Help view
import Help from '@/views/help/Help.vue'
import Documentation from '@/views/help/Documentation.vue'

// Plugin views
const IncidentsList = () => import('@/plugins/incidents/views/IncidentsList.vue')
const Accounting = () => import('@/plugins/accounting/views/Accounting.vue')
const Inventory = () => import('@/plugins/inventory/views/Inventory.vue')
const Performance = () => import('@/plugins/performance/views/Performance.vue')
const Security = () => import('@/plugins/security/views/Security.vue')
const Configuration = () => import('@/plugins/configuration/views/Configuration.vue')

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/auth/signin',
    name: 'SignIn',
    component: SignIn,
    meta: { guest: true }
  },
  {
    path: '/auth/signup',
    name: 'SignUp',
    component: SignUp,
    meta: { guest: true }
  },
  {
    path: '/auth/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { guest: true }
  },
  {
    path: '/',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'users',
        name: 'Users',
        component: Users,
        meta: { requiresAdmin: true }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        children: [
          {
            path: '',
            redirect: '/settings/profile'
          },
          {
            path: 'profile',
            name: 'SettingsProfile',
            component: Profile
          },
          {
            path: 'account',
            name: 'SettingsAccount',
            component: Account
          },
          {
            path: 'notifications',
            name: 'SettingsNotifications',
            component: Notifications
          },
          {
            path: 'display',
            name: 'SettingsDisplay',
            component: Display
          }
        ]
      },
      {
        path: 'help',
        name: 'Help',
        component: Help
      },
      {
        path: 'help/documentation',
        name: 'Documentation',
        component: Documentation
      },
      // Plugin routes
      {
        path: 'plugins/incidents',
        name: 'PluginsIncidents',
        component: IncidentsList
      },
      {
        path: 'plugins/accounting',
        name: 'PluginsAccounting',
        component: Accounting
      },
      {
        path: 'plugins/inventory',
        name: 'PluginsInventory',
        component: Inventory
      },
      {
        path: 'plugins/performance',
        name: 'PluginsPerformance',
        component: Performance
      },
      {
        path: 'plugins/security',
        name: 'PluginsSecurity',
        component: Security
      },
      {
        path: 'plugins/configuration',
        name: 'PluginsConfiguration',
        component: Configuration
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/auth/signin')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/dashboard')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
