<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardFooter from '@/components/ui/CardFooter.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref(null)
const credentials = ref({
  username: '',
  password: ''
})

async function handleLogin() {
  loading.value = true
  error.value = null
  
  const success = await authStore.login(credentials.value)
  
  if (success) {
    router.push('/dashboard')
  } else {
    error.value = authStore.error || 'Login failed'
  }
  
  loading.value = false
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-background">
    <Card class="w-full max-w-md">
      <CardHeader class="space-y-1">
        <CardTitle class="text-2xl font-bold">Sign In</CardTitle>
        <CardDescription>
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div v-if="error" class="p-3 text-sm text-destructive bg-destructive/10 rounded-lg">
            {{ error }}
          </div>
          <div class="space-y-2">
            <Label for="username">Username</Label>
            <Input
              id="username"
              v-model="credentials.username"
              type="text"
              placeholder="Enter your username"
              required
              :disabled="loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input
              id="password"
              v-model="credentials.password"
              type="password"
              placeholder="Enter your password"
              required
              :disabled="loading"
            />
          </div>
          <Button 
            type="submit" 
            class="w-full" 
            :disabled="loading"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </Button>
        </form>
      </CardContent>
      <CardFooter class="flex flex-col space-y-2">
        <RouterLink 
          to="/auth/forgot-password" 
          class="text-sm text-muted-foreground hover:text-foreground"
        >
          Forgot password?
        </RouterLink>
        <p class="text-sm text-muted-foreground">
          Don't have an account? 
          <RouterLink to="/auth/signup" class="text-primary hover:underline">
            Sign up
          </RouterLink>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>
