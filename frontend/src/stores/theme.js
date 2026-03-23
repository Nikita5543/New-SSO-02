import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // Always start with 'light' theme - no localStorage read on init
  // Theme will be updated from user profile after login
  const theme = ref('light')
  const background = ref(null)
  const systemTheme = ref(
    window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  )

  const effectiveTheme = computed(() => {
    if (theme.value === 'system') return systemTheme.value
    return theme.value
  })

  const isDark = computed(() => effectiveTheme.value === 'dark')
  const hasBackground = computed(() => !!background.value)

  function setTheme(newTheme) {
    theme.value = newTheme
    applyTheme()
  }

  function setBackground(filename) {
    background.value = filename
    applyBackground()
  }

  function applyTheme() {
    const root = document.documentElement
    if (effectiveTheme.value === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }

  function applyBackground() {
    const body = document.body
    if (background.value) {
      body.style.backgroundImage = `url('/backgrounds/${background.value}')`
      body.style.backgroundSize = 'cover'
      body.style.backgroundPosition = 'center'
      body.style.backgroundAttachment = 'fixed'
      body.style.backgroundRepeat = 'no-repeat'
      document.documentElement.classList.add('has-bg')
    } else {
      body.style.backgroundImage = ''
      body.style.backgroundSize = ''
      body.style.backgroundPosition = ''
      body.style.backgroundAttachment = ''
      body.style.backgroundRepeat = ''
      document.documentElement.classList.remove('has-bg')
    }
  }

  function initTheme() {
    // Always apply light theme on startup - will be overridden from user profile
    theme.value = 'light'
    background.value = null
    
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      systemTheme.value = e.matches ? 'dark' : 'light'
      if (theme.value === 'system') applyTheme()
    })
    applyTheme()
    applyBackground()
  }

  // Apply user preferences from their profile
  function applyUserPreferences(user) {
    if (!user) return
    // Apply theme from user profile if saved
    if (user.theme) {
      theme.value = user.theme
      applyTheme()
    }
    // Apply background from user profile if saved
    if (user.background_image) {
      background.value = user.background_image
      applyBackground()
    }
  }

  watch(theme, applyTheme)

  return {
    theme,
    background,
    systemTheme,
    effectiveTheme,
    isDark,
    hasBackground,
    setTheme,
    setBackground,
    initTheme,
    applyBackground,
    applyUserPreferences,
  }
})

