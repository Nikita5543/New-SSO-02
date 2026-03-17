<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Activity } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Performance</h1>
      <p class="text-muted-foreground mt-1">Network performance monitoring</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Activity class="h-5 w-5" />
          Performance Module
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm">Performance monitoring features coming soon...</p>
        <ul class="mt-4 space-y-2 text-sm text-muted-foreground">
          <li>• Performance targets</li>
          <li>• Metrics collection</li>
          <li>• Threshold alerts</li>
        </ul>
      </CardContent>
    </Card>
  </div>
</template>
