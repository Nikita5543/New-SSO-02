<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Sidebar from '@/components/layout/Sidebar.vue'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import DropdownMenuItem from '@/components/ui/DropdownMenuItem.vue'
import DropdownMenuSeparator from '@/components/ui/DropdownMenuSeparator.vue'
import Avatar from '@/components/ui/Avatar.vue'
import { Menu, X, LogOut, User, Settings } from 'lucide-vue-next'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()
const sidebarOpen = ref(false)

onMounted(() => {
  themeStore.applyBackground()
})

async function handleLogout() {
  await authStore.logout()
  router.push('/auth/signin')
}
</script>

<template>
  <div class="flex h-screen overflow-hidden" :class="themeStore.hasBackground ? 'bg-transparent' : 'bg-background'">
    <!-- Sidebar (desktop) -->
    <aside
      class="hidden w-64 shrink-0 border-r lg:block"
      :class="themeStore.hasBackground
        ? 'bg-black/40 backdrop-blur-md border-white/10'
        : 'bg-card'"
    >
      <Sidebar :has-background="themeStore.hasBackground" />
    </aside>

    <!-- Mobile sidebar overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 z-40 bg-black/50 lg:hidden"
        @click="sidebarOpen = false"
      />
    </Transition>

    <!-- Mobile sidebar -->
    <Transition
      enter-active-class="transition-transform duration-300 ease-out"
      enter-from-class="-translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition-transform duration-300 ease-in"
      leave-from-class="translate-x-0"
      leave-to-class="-translate-x-full"
    >
      <aside
        v-if="sidebarOpen"
        class="fixed inset-y-0 left-0 z-50 w-64 border-r lg:hidden"
        :class="themeStore.hasBackground
          ? 'bg-black/50 backdrop-blur-md border-white/10'
          : 'bg-card'"
      >
        <Sidebar @close="sidebarOpen = false" :has-background="themeStore.hasBackground" />
      </aside>
    </Transition>

    <!-- Main content -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Header -->
      <header
        class="flex h-14 items-center gap-4 border-b px-4 lg:px-6"
        :class="themeStore.hasBackground
          ? 'bg-black/50 backdrop-blur-md border-white/10 text-white'
          : 'bg-card'"
      >
        <!-- Mobile menu button -->
        <button
          class="inline-flex items-center justify-center rounded-md p-2 hover:bg-white/10 lg:hidden"
          :class="themeStore.hasBackground ? 'text-white' : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'"
          @click="sidebarOpen = !sidebarOpen"
        >
          <Menu v-if="!sidebarOpen" class="h-5 w-5" />
          <X v-else class="h-5 w-5" />
        </button>

        <div class="flex-1" />

        <!-- Theme toggle -->
        <ThemeToggle />

        <!-- User dropdown -->
        <DropdownMenu>
          <template #trigger>
            <button
              class="flex items-center gap-2 rounded-md p-1"
              :class="themeStore.hasBackground ? 'hover:bg-white/10' : 'hover:bg-accent'"
            >
              <!-- Avatar with system or custom image -->
              <div v-if="authStore.user?.avatar_url && authStore.user.avatar_url.startsWith('system:')"
                   class="h-8 w-8 overflow-hidden rounded-full">
                <img :src="`/avatars/avatar-${authStore.user.avatar_url.split(':')[1]}.svg`"
                     alt="Avatar" class="h-full w-full object-cover" />
              </div>
              <div v-else-if="authStore.user?.avatar_url" class="h-8 w-8 overflow-hidden rounded-full">
                <img :src="authStore.user.avatar_url" alt="Avatar" class="h-full w-full object-cover" />
              </div>
              <Avatar v-else
                :alt="authStore.user?.full_name || authStore.user?.username"
                size="sm"
              />
            </button>
          </template>
          <template #default="{ close }">
            <div class="px-2 py-1.5">
              <p class="text-sm font-medium">
                {{ authStore.user?.full_name || authStore.user?.username }}
              </p>
              <p class="text-xs text-muted-foreground">
                {{ authStore.user?.email }}
              </p>
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="router.push('/settings/profile'); close()">
              <User class="mr-2 h-4 w-4" />
              Profile
            </DropdownMenuItem>
            <DropdownMenuItem @click="router.push('/settings'); close()">
              <Settings class="mr-2 h-4 w-4" />
              Settings
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="handleLogout(); close()">
              <LogOut class="mr-2 h-4 w-4" />
              Log out
            </DropdownMenuItem>
          </template>
        </DropdownMenu>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-auto p-4 lg:p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
