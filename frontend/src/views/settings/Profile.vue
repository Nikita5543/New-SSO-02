<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Label from '@/components/ui/Label.vue'
import { User, Upload, Check } from 'lucide-vue-next'

const authStore = useAuthStore()
const selectedAvatar = ref(authStore.user?.avatar_url || null)
const isUpdating = ref(false)
const updateSuccess = ref(false)

// System avatars configuration
const systemAvatars = [
  { id: 'system:1', name: 'Gradient Purple', src: '/avatars/avatar-1.svg' },
  { id: 'system:2', name: 'Smiley Green', src: '/avatars/avatar-2.svg' },
  { id: 'system:3', name: 'Abstract Pink', src: '/avatars/avatar-3.svg' },
]

// Get current avatar URL
const currentAvatarUrl = computed(() => {
  if (!selectedAvatar.value) return null
  if (selectedAvatar.value.startsWith('system:')) {
    const avatar = systemAvatars.find(a => a.id === selectedAvatar.value)
    return avatar?.src
  }
  return selectedAvatar.value
})

// Get initials for fallback
const userInitials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.username || '?'
  return name.charAt(0).toUpperCase()
})

function selectSystemAvatar(avatarId) {
  selectedAvatar.value = avatarId
  updateSuccess.value = false
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // For now, create a local URL (in production, upload to server)
  const reader = new FileReader()
  reader.onload = (e) => {
    selectedAvatar.value = e.target.result
    updateSuccess.value = false
  }
  reader.readAsDataURL(file)
}

async function saveAvatar() {
  isUpdating.value = true
  updateSuccess.value = false
  
  try {
    const response = await authStore.authFetch('/api/v1/users/me/avatar', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ avatar_url: selectedAvatar.value })
    })
    
    if (response.ok) {
      // Update local user data
      authStore.user.avatar_url = selectedAvatar.value
      updateSuccess.value = true
    }
  } catch (e) {
    console.error('Failed to update avatar:', e)
  } finally {
    isUpdating.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h2 class="text-2xl font-bold">Profile</h2>
      <p class="text-muted-foreground">Manage your profile information and avatar</p>
    </div>

    <!-- User Info Card -->
    <Card>
      <CardHeader>
        <CardTitle>Personal Information</CardTitle>
        <CardDescription>Your account details</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="space-y-2">
            <Label>Username</Label>
            <p class="text-sm font-medium">{{ authStore.user?.username }}</p>
          </div>
          <div class="space-y-2">
            <Label>Email</Label>
            <p class="text-sm font-medium">{{ authStore.user?.email }}</p>
          </div>
          <div class="space-y-2">
            <Label>Full Name</Label>
            <p class="text-sm font-medium">{{ authStore.user?.full_name || 'Not set' }}</p>
          </div>
          <div class="space-y-2">
            <Label>Role</Label>
            <p class="text-sm font-medium capitalize">{{ authStore.user?.role }}</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Avatar Selection Card -->
    <Card>
      <CardHeader>
        <CardTitle>Profile Picture</CardTitle>
        <CardDescription>Choose a system avatar or upload your own</CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- Current Avatar Preview -->
        <div class="flex items-center gap-4">
          <div class="relative">
            <div v-if="currentAvatarUrl" class="h-20 w-20 overflow-hidden rounded-full">
              <img :src="currentAvatarUrl" alt="Avatar" class="h-full w-full object-cover" />
            </div>
            <div v-else class="flex h-20 w-20 items-center justify-center rounded-full bg-muted text-2xl font-bold">
              {{ userInitials }}
            </div>
          </div>
          <div>
            <p class="font-medium">Current Avatar</p>
            <p class="text-sm text-muted-foreground">
              {{ selectedAvatar?.startsWith('system:') ? 'System avatar' : selectedAvatar ? 'Custom upload' : 'Default initials' }}
            </p>
          </div>
        </div>

        <!-- System Avatars -->
        <div class="space-y-3">
          <Label>System Avatars</Label>
          <div class="flex flex-wrap gap-4">
            <button
              v-for="avatar in systemAvatars"
              :key="avatar.id"
              @click="selectSystemAvatar(avatar.id)"
              :class="[
                'relative h-16 w-16 overflow-hidden rounded-full transition-all hover:scale-105',
                selectedAvatar === avatar.id ? 'ring-2 ring-primary ring-offset-2' : 'ring-1 ring-border'
              ]"
              :title="avatar.name"
            >
              <img :src="avatar.src" :alt="avatar.name" class="h-full w-full object-cover" />
              <div v-if="selectedAvatar === avatar.id" class="absolute inset-0 flex items-center justify-center bg-primary/20">
                <Check class="h-6 w-6 text-primary" />
              </div>
            </button>
          </div>
        </div>

        <!-- Custom Upload -->
        <div class="space-y-3">
          <Label>Custom Avatar</Label>
          <div class="flex items-center gap-4">
            <label class="cursor-pointer">
              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleFileUpload"
              />
              <Button type="button" variant="outline">
                <Upload class="mr-2 h-4 w-4" />
                Upload Image
              </Button>
            </label>
            <p class="text-sm text-muted-foreground">JPG, PNG or GIF. Max 2MB.</p>
          </div>
        </div>

        <!-- Save Button -->
        <div class="flex items-center gap-4">
          <Button @click="saveAvatar" :disabled="isUpdating">
            <User v-if="!isUpdating" class="mr-2 h-4 w-4" />
            <span v-if="isUpdating">Saving...</span>
            <span v-else>Save Avatar</span>
          </Button>
          <p v-if="updateSuccess" class="text-sm text-green-600">Avatar updated successfully!</p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
