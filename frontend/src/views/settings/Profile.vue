<script setup>
import { useAuthStore } from '@/stores/auth'
import Label from '@/components/ui/Label.vue'

const authStore = useAuthStore()
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-2xl font-bold">Profile</h2>
    <div class="space-y-2">
      <Label>Username</Label>
      <p class="text-sm">{{ authStore.user?.username }}</p>
    </div>
    <div class="space-y-2">
      <Label>Email</Label>
      <p class="text-sm">{{ authStore.user?.email }}</p>
    </div>
    <div class="space-y-2">
      <Label>Full Name</Label>
      <p class="text-sm">{{ authStore.user?.full_name || 'Not set' }}</p>
    </div>
  </div>
</template>
