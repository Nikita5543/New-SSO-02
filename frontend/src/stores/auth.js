import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useThemeStore } from './theme'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('accessToken') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const tokenExpiry = ref(localStorage.getItem('tokenExpiry') || null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => {
    // Проверяем наличие токена и не истёк ли он
    if (!accessToken.value || !tokenExpiry.value) return false
    const now = new Date().getTime()
    return now < parseInt(tokenExpiry.value)
  })
  
  const isAdmin = computed(() => user.value?.role === 'superuser')
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
      
      // Apply user's theme and background preferences from profile
      useThemeStore().applyUserPreferences(data.user)
      
      // Сохраняем токены на 3 часа (10800 секунд)
      const expiryTime = new Date().getTime() + (3 * 60 * 60 * 1000)
      localStorage.setItem('accessToken', data.access_token)
      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('tokenExpiry', expiryTime.toString())
      tokenExpiry.value = expiryTime.toString()
      
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
      const response = await fetch('/api/v1/auth/register', {
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
      
      // Обновляем время экспирации
      const expiryTime = new Date().getTime() + (3 * 60 * 60 * 1000)
      localStorage.setItem('accessToken', data.access_token)
      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('tokenExpiry', expiryTime.toString())
      tokenExpiry.value = expiryTime.toString()
      
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
    tokenExpiry.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('tokenExpiry')
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
    tokenExpiry,
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
