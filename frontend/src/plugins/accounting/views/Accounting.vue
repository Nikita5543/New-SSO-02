<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { DollarSign } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Accounting</h1>
      <p class="text-muted-foreground mt-1">Traffic accounting and billing</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <DollarSign class="h-5 w-5" />
          Accounting Module
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm">Accounting features coming soon...</p>
        <ul class="mt-4 space-y-2 text-sm text-muted-foreground">
          <li>• Interface traffic tracking</li>
          <li>• Bandwidth usage reports</li>
          <li>• Billing calculations</li>
        </ul>
      </CardContent>
    </Card>
  </div>
</template>
