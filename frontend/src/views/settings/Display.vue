<script setup>
import { ref, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Sun, Moon, Monitor, Check, X } from 'lucide-vue-next'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const saving = ref(false)
const saveMsg = ref('')

// List of available backgrounds - served from /backgrounds/ by nginx
// Add filenames here when you put new images in frontend/public/backgrounds/
const backgrounds = ref([
  'bg1.avif',
  'bg2.avif',
  'bg3.avif',
  'bg4.avif',
  'bg5.avif',
  'bg6.avif',
  'bg7.webp',
  'bg8.jpg',
])

onMounted(async () => {
  // Sync background from user profile if not in localStorage
  if (authStore.user?.background_image && !themeStore.background) {
    themeStore.setBackground(authStore.user.background_image)
  }
})

async function selectBackground(filename) {
  saving.value = true
  saveMsg.value = ''
  try {
    const resp = await authStore.authFetch('/api/v1/users/me/background', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ background_image: filename })
    })
    if (resp.ok) {
      const userData = await resp.json()
      authStore.user = userData
      themeStore.setBackground(filename)
      saveMsg.value = 'saved'
    }
  } finally {
    saving.value = false
    setTimeout(() => saveMsg.value = '', 2000)
  }
}

async function clearBackground() {
  saving.value = true
  try {
    const resp = await authStore.authFetch('/api/v1/users/me/background', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ background_image: null })
    })
    if (resp.ok) {
      const userData = await resp.json()
      authStore.user = userData
      themeStore.setBackground(null)
    }
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold">Display</h2>

    <!-- Theme selection -->
    <Card>
      <CardContent class="p-6">
        <h3 class="text-lg font-semibold mb-4">Color Theme</h3>
        <div class="flex gap-3 flex-wrap">
          <button
            @click="themeStore.setTheme('light')"
            :class="[
              'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all',
              themeStore.theme === 'light'
                ? 'border-primary bg-primary/10'
                : 'border-border hover:border-primary/50'
            ]"
          >
            <Sun class="h-6 w-6" />
            <span class="text-sm font-medium">Light</span>
            <Check v-if="themeStore.theme === 'light'" class="h-4 w-4 text-primary" />
          </button>

          <button
            @click="themeStore.setTheme('dark')"
            :class="[
              'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all',
              themeStore.theme === 'dark'
                ? 'border-primary bg-primary/10'
                : 'border-border hover:border-primary/50'
            ]"
          >
            <Moon class="h-6 w-6" />
            <span class="text-sm font-medium">Dark</span>
            <Check v-if="themeStore.theme === 'dark'" class="h-4 w-4 text-primary" />
          </button>

          <button
            @click="themeStore.setTheme('system')"
            :class="[
              'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all',
              themeStore.theme === 'system'
                ? 'border-primary bg-primary/10'
                : 'border-border hover:border-primary/50'
            ]"
          >
            <Monitor class="h-6 w-6" />
            <span class="text-sm font-medium">System</span>
            <Check v-if="themeStore.theme === 'system'" class="h-4 w-4 text-primary" />
          </button>
        </div>
      </CardContent>
    </Card>

    <!-- Background selection -->
    <Card>
      <CardContent class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Background Image</h3>
            <p class="text-sm text-muted-foreground">Choose a background for your dashboard</p>
          </div>
          <button
            v-if="themeStore.background"
            @click="clearBackground"
            class="flex items-center gap-1 text-sm text-destructive hover:underline"
          >
            <X class="h-4 w-4" /> Remove background
          </button>
        </div>

        <!-- No backgrounds available -->
        <div v-if="backgrounds.length === 0" class="text-center py-8 text-muted-foreground">
          <p class="text-sm">No backgrounds available yet.</p>
          <p class="text-xs mt-1">Place image files in <code class="bg-muted px-1 rounded">/public/backgrounds/</code></p>
        </div>

        <!-- Background grid -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          <button
            v-for="bg in backgrounds"
            :key="bg"
            @click="selectBackground(bg)"
            :class="[
              'relative rounded-xl overflow-hidden border-2 transition-all aspect-video',
              themeStore.background === bg
                ? 'border-primary ring-2 ring-primary/50'
                : 'border-border hover:border-primary/50'
            ]"
          >
            <img
              :src="`/backgrounds/${bg}`"
              :alt="bg"
              class="w-full h-full object-cover"
            />
            <div v-if="themeStore.background === bg"
                 class="absolute inset-0 bg-primary/20 flex items-center justify-center">
              <Check class="h-6 w-6 text-white drop-shadow" />
            </div>
            <div class="absolute bottom-0 left-0 right-0 bg-black/40 px-2 py-1">
              <p class="text-white text-xs truncate">{{ bg }}</p>
            </div>
          </button>
        </div>

        <p v-if="saveMsg === 'saved'" class="mt-3 text-sm text-green-600 font-medium">✓ Background saved!</p>
      </CardContent>
    </Card>
  </div>
</template>
