<script setup>
import { RouterLink } from 'vue-router'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import { AlertTriangle } from 'lucide-vue-next'
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-background">
    <Card class="w-full max-w-md">
      <CardHeader class="text-center">
        <AlertTriangle class="h-16 w-16 mx-auto text-destructive" />
        <CardTitle class="text-4xl mt-4">404</CardTitle>
        <p class="text-muted-foreground">Page not found</p>
      </CardHeader>
      <CardContent class="text-center">
        <p class="mb-4 text-sm text-muted-foreground">
          The page you're looking for doesn't exist.
        </p>
        <RouterLink to="/dashboard">
          <Button>Go to Dashboard</Button>
        </RouterLink>
      </CardContent>
    </Card>
  </div>
</template>
