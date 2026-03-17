<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Settings } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Configuration</h1>
      <p class="text-muted-foreground mt-1">Configuration management</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Settings class="h-5 w-5" />
          Configuration Module
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm">Configuration features coming soon...</p>
        <ul class="mt-4 space-y-2 text-sm text-muted-foreground">
          <li>• Configuration snapshots</li>
          <li>• Templates</li>
          <li>• Change tracking</li>
        </ul>
      </CardContent>
    </Card>
  </div>
</template>
