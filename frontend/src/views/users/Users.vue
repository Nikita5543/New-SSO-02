<script setup>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Users as UsersIcon } from 'lucide-vue-next'

const users = ref([])
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Users</h1>
      <p class="text-muted-foreground mt-1">Manage system users</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <UsersIcon class="h-5 w-5" />
          All Users
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm text-muted-foreground">User management coming soon...</p>
      </CardContent>
    </Card>
  </div>
</template>
