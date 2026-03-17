<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-2xl font-bold">Account</h2>
    <div class="space-y-2">
      <p class="text-sm"><strong>Role:</strong> {{ authStore.user?.role }}</p>
      <p class="text-sm"><strong>Member since:</strong> {{ new Date().toLocaleDateString() }}</p>
    </div>
  </div>
</template>
