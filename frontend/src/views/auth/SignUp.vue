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
const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

async function handleRegister() {
  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    await authStore.register({
      username: formData.value.username,
      email: formData.value.email,
      password: formData.value.password
    })
    
    router.push('/auth/signin')
  } catch (e) {
    error.value = e.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-background">
    <Card class="w-full max-w-md">
      <CardHeader class="space-y-1">
        <CardTitle class="text-2xl font-bold">Create Account</CardTitle>
        <CardDescription>
          Enter your details to create a new account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div v-if="error" class="p-3 text-sm text-destructive bg-destructive/10 rounded-lg">
            {{ error }}
          </div>
          <div class="space-y-2">
            <Label for="username">Username</Label>
            <Input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="Choose a username"
              required
              :disabled="loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="Enter your email"
              required
              :disabled="loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input
              id="password"
              v-model="formData.password"
              type="password"
              placeholder="Create a password"
              required
              :disabled="loading"
            />
          </div>
          <div class="space-y-2">
            <Label for="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              placeholder="Confirm your password"
              required
              :disabled="loading"
            />
          </div>
          <Button 
            type="submit" 
            class="w-full" 
            :disabled="loading"
          >
            {{ loading ? 'Creating account...' : 'Sign Up' }}
          </Button>
        </form>
      </CardContent>
      <CardFooter>
        <p class="text-sm text-muted-foreground w-full text-center">
          Already have an account? 
          <RouterLink to="/auth/signin" class="text-primary hover:underline">
            Sign in
          </RouterLink>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>
