<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { User, CreditCard, Bell, Monitor } from 'lucide-vue-next'

const menuItems = [
  { title: 'Profile', path: '/settings/profile', icon: User },
  { title: 'Account', path: '/settings/account', icon: CreditCard },
  { title: 'Notifications', path: '/settings/notifications', icon: Bell },
  { title: 'Display', path: '/settings/display', icon: Monitor },
]
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Settings</h1>
      <p class="text-muted-foreground mt-1">Manage your account settings</p>
    </div>

    <div class="grid gap-6 md:grid-cols-[200px_1fr]">
      <Card>
        <CardContent class="p-4 space-y-1">
          <RouterLink
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent"
          >
            <component :is="item.icon" class="h-4 w-4" />
            {{ item.title }}
          </RouterLink>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="p-6">
          <RouterView />
        </CardContent>
      </Card>
    </div>
  </div>
</template>
