<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Badge from '@/components/ui/Badge.vue'
import { Users, UserPlus, Edit, Trash2, RefreshCw, Shield, UserCog } from 'lucide-vue-next'

const authStore = useAuthStore()
const users = ref([])
const loading = ref(false)
const error = ref(null)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedUser = ref(null)

const formData = ref({
  username: '',
  email: '',
  password: '',
  full_name: '',
  role: 'user',
  is_active: true
})

async function fetchUsers() {
  loading.value = true
  error.value = null
  try {
    const response = await authStore.authFetch('/api/v1/users/')
    if (response.ok) {
      users.value = await response.json()
    }
  } catch (e) {
    error.value = 'Failed to load users'
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function createUser() {
  try {
    const response = await authStore.authFetch('/api/v1/users/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    
    if (response.ok) {
      await fetchUsers()
      showCreateModal.value = false
      resetForm()
    }
  } catch (e) {
    error.value = 'Failed to create user'
    console.error(e)
  }
}

async function updateUser() {
  if (!selectedUser.value) return
  
  try {
    const response = await authStore.authFetch(`/api/v1/users/${selectedUser.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    
    if (response.ok) {
      await fetchUsers()
      showEditModal.value = false
      selectedUser.value = null
      resetForm()
    }
  } catch (e) {
    error.value = 'Failed to update user'
    console.error(e)
  }
}

async function deleteUser(userId) {
  if (!confirm('Are you sure you want to delete this user?')) return
  
  try {
    const response = await authStore.authFetch(`/api/v1/users/${userId}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      await fetchUsers()
    }
  } catch (e) {
    error.value = 'Failed to delete user'
    console.error(e)
  }
}

function openEditModal(user) {
  selectedUser.value = user
  formData.value = {
    username: user.username,
    email: user.email,
    password: '',
    full_name: user.full_name || '',
    role: user.role,
    is_active: user.is_active
  }
  showEditModal.value = true
}

function openCreateModal() {
  resetForm()
  showCreateModal.value = true
}

function resetForm() {
  formData.value = {
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'user',
    is_active: true
  }
}

function getRoleBadgeVariant(role) {
  if (role === 'superuser') return 'default'
  return 'secondary'
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Users Management</h1>
        <p class="text-muted-foreground mt-1">Manage system users and their roles</p>
      </div>
      <Button @click="openCreateModal">
        <UserPlus class="h-4 w-4 mr-2" />
        Add User
      </Button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="rounded-lg bg-destructive/10 p-4 text-destructive">
      {{ error }}
    </div>

    <!-- Users Table -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>System Users</CardTitle>
            <CardDescription>All registered users in the system</CardDescription>
          </div>
          <Button variant="outline" @click="fetchUsers" :disabled="loading">
            <RefreshCw :class="['h-4 w-4 mr-2', loading ? 'animate-spin' : '']" />
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="loading" class="flex items-center justify-center py-12">
          <RefreshCw class="h-8 w-8 animate-spin text-muted-foreground" />
        </div>

        <div v-else-if="users.length === 0" class="text-center py-12 text-muted-foreground">
          <Users class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold">No users found</h3>
          <p class="text-sm mt-1">Create a new user to get started</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b bg-muted/50">
                <th class="px-4 py-3 text-left font-medium">Username</th>
                <th class="px-4 py-3 text-left font-medium">Email</th>
                <th class="px-4 py-3 text-left font-medium">Full Name</th>
                <th class="px-4 py-3 text-left font-medium">Role</th>
                <th class="px-4 py-3 text-left font-medium">Status</th>
                <th class="px-4 py-3 text-left font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="user in users"
                :key="user.id"
                class="border-b last:border-b-0 hover:bg-muted/50 transition-colors"
              >
                <td class="px-4 py-3 font-medium">{{ user.username }}</td>
                <td class="px-4 py-3">{{ user.email }}</td>
                <td class="px-4 py-3 text-muted-foreground">{{ user.full_name || '—' }}</td>
                <td class="px-4 py-3">
                  <Badge :variant="getRoleBadgeVariant(user.role)">
                    <Shield v-if="user.role === 'superuser'" class="h-3 w-3 mr-1 inline" />
                    {{ user.role }}
                  </Badge>
                </td>
                <td class="px-4 py-3">
                  <Badge :variant="user.is_active ? 'default' : 'secondary'">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </Badge>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <Button
                      size="sm"
                      variant="ghost"
                      @click="openEditModal(user)"
                    >
                      <Edit class="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      @click="deleteUser(user.id)"
                      :disabled="user.id === authStore.user?.id"
                    >
                      <Trash2 class="h-4 w-4" />
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>

    <!-- Create User Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click="showCreateModal = false"
    >
      <Card class="w-full max-w-md m-4" @click.stop>
        <CardHeader>
          <CardTitle>Add New User</CardTitle>
          <CardDescription>Create a new system user</CardDescription>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="createUser" class="space-y-4">
            <div>
              <Label for="username">Username</Label>
              <Input
                id="username"
                v-model="formData.username"
                placeholder="Enter username"
                required
              />
            </div>
            <div>
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="formData.email"
                type="email"
                placeholder="Enter email"
                required
              />
            </div>
            <div>
              <Label for="password">Password</Label>
              <Input
                id="password"
                v-model="formData.password"
                type="password"
                placeholder="Enter password"
                required
              />
            </div>
            <div>
              <Label for="full_name">Full Name</Label>
              <Input
                id="full_name"
                v-model="formData.full_name"
                placeholder="Enter full name"
              />
            </div>
            <div>
              <Label for="role">Role</Label>
              <select
                id="role"
                v-model="formData.role"
                class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="user">User</option>
                <option value="superuser">Superuser</option>
              </select>
            </div>
            <div class="flex items-center gap-2">
              <input
                type="checkbox"
                id="is_active"
                v-model="formData.is_active"
                class="rounded"
              />
              <Label for="is_active">Active</Label>
            </div>
            <div class="flex gap-2">
              <Button type="submit" class="flex-1">Create User</Button>
              <Button type="button" variant="outline" @click="showCreateModal = false">
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>

    <!-- Edit User Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click="showEditModal = false"
    >
      <Card class="w-full max-w-md m-4" @click.stop>
        <CardHeader>
          <CardTitle>Edit User</CardTitle>
          <CardDescription>Update user information</CardDescription>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="updateUser" class="space-y-4">
            <div>
              <Label for="edit-username">Username</Label>
              <Input
                id="edit-username"
                v-model="formData.username"
                disabled
              />
            </div>
            <div>
              <Label for="edit-email">Email</Label>
              <Input
                id="edit-email"
                v-model="formData.email"
                type="email"
                required
              />
            </div>
            <div>
              <Label for="edit-password">New Password (leave empty to keep current)</Label>
              <Input
                id="edit-password"
                v-model="formData.password"
                type="password"
                placeholder="Enter new password"
              />
            </div>
            <div>
              <Label for="edit-full_name">Full Name</Label>
              <Input
                id="edit-full_name"
                v-model="formData.full_name"
                placeholder="Enter full name"
              />
            </div>
            <div>
              <Label for="edit-role">Role</Label>
              <select
                id="edit-role"
                v-model="formData.role"
                class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="user">User</option>
                <option value="superuser">Superuser</option>
              </select>
            </div>
            <div class="flex items-center gap-2">
              <input
                type="checkbox"
                id="edit-is_active"
                v-model="formData.is_active"
                class="rounded"
              />
              <Label for="edit-is_active">Active</Label>
            </div>
            <div class="flex gap-2">
              <Button type="submit" class="flex-1">Save Changes</Button>
              <Button type="button" variant="outline" @click="showEditModal = false">
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
