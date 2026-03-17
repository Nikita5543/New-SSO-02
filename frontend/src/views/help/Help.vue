<script setup>
import { RouterLink } from 'vue-router'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { HelpCircle, BookOpen } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Help & Support</h1>
      <p class="text-muted-foreground mt-1">Get help with NOC Vision</p>
    </div>

    <div class="grid gap-4 md:grid-cols-2">
      <RouterLink to="/help/documentation">
        <Card class="hover:bg-accent transition-colors cursor-pointer">
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <BookOpen class="h-5 w-5" />
              Documentation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-sm text-muted-foreground">
              Complete guide for creating and managing plugins
            </p>
          </CardContent>
        </Card>
      </RouterLink>

      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <HelpCircle class="h-5 w-5" />
            Support
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground">
            Contact support for assistance
          </p>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
