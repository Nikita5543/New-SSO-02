import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('accessToken') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userRole = computed(() => user.value?.role || 'user')

  function hasRole(role) {
    if (Array.isArray(role)) {
      return role.includes(user.value?.role)
    }
    return user.value?.role === role
  }

  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const formData = new URLSearchParams()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Login failed')
      }

      const data = await response.json()
      accessToken.value = data.access_token
      refreshToken.value = data.refresh_token
      user.value = data.user
      localStorage.setItem('accessToken', data.access_token)
      localStorage.setItem('refreshToken', data.refresh_token)
      return true
    } catch (e) {
      error.value = e.message
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      const response = await authFetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      })
      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Registration failed')
      }
      return await response.json()
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!accessToken.value) return
    try {
      const response = await authFetch('/api/v1/auth/me')
      if (response.ok) {
        user.value = await response.json()
      } else {
        await logout()
      }
    } catch {
      await logout()
    }
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) return false
    try {
      const response = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken.value }),
      })
      if (!response.ok) {
        await logout()
        return false
      }
      const data = await response.json()
      accessToken.value = data.access_token
      refreshToken.value = data.refresh_token
      user.value = data.user
      localStorage.setItem('accessToken', data.access_token)
      localStorage.setItem('refreshToken', data.refresh_token)
      return true
    } catch {
      await logout()
      return false
    }
  }

  async function logout() {
    if (refreshToken.value && accessToken.value) {
      try {
        await fetch('/api/v1/auth/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${accessToken.value}`,
          },
          body: JSON.stringify({ refresh_token: refreshToken.value }),
        })
      } catch {
        // Ignore logout errors
      }
    }
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  async function authFetch(url, options = {}) {
    if (!options.headers) options.headers = {}
    if (accessToken.value) {
      options.headers.Authorization = `Bearer ${accessToken.value}`
    }

    let response = await fetch(url, options)

    if (response.status === 401 && refreshToken.value) {
      const refreshed = await refreshAccessToken()
      if (refreshed) {
        options.headers.Authorization = `Bearer ${accessToken.value}`
        response = await fetch(url, options)
      }
    }

    return response
  }

  return {
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    userRole,
    hasRole,
    login,
    register,
    fetchUser,
    refreshAccessToken,
    logout,
    authFetch,
  }
})
