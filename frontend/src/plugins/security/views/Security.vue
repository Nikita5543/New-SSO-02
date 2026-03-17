<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Shield } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Security</h1>
      <p class="text-muted-foreground mt-1">Security monitoring and events</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Shield class="h-5 w-5" />
          Security Module
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm">Security features coming soon...</p>
        <ul class="mt-4 space-y-2 text-sm text-muted-foreground">
          <li>• Audit logs</li>
          <li>• Security events</li>
          <li>• Access monitoring</li>
        </ul>
      </CardContent>
    </Card>
  </div>
</template>
