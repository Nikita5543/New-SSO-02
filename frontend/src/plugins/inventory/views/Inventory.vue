<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { Package } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Inventory</h1>
      <p class="text-muted-foreground mt-1">Equipment inventory management</p>
    </div>

    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Package class="h-5 w-5" />
          Inventory Module
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm">Inventory features coming soon...</p>
        <ul class="mt-4 space-y-2 text-sm text-muted-foreground">
          <li>• Device management</li>
          <li>• Site organization</li>
          <li>• Equipment tracking</li>
        </ul>
      </CardContent>
    </Card>
  </div>
</template>
