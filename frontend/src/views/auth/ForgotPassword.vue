<script setup>
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import { Monitor } from 'lucide-vue-next'
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-background p-4">
    <Card class="w-full max-w-md">
      <CardHeader class="text-center">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary">
          <Monitor class="h-6 w-6 text-primary-foreground" />
        </div>
        <CardTitle>Forgot Password</CardTitle>
        <CardDescription>Password recovery is not available in this version. Please contact your administrator.</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="text-center">
          <RouterLink to="/auth/signin">
            <Button variant="outline">Back to Sign In</Button>
          </RouterLink>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
