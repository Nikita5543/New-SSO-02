import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref(localStorage.getItem('theme') || 'light')
  const background = ref(localStorage.getItem('background') || null)
  const systemTheme = ref(
    window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  )

  const effectiveTheme = computed(() => {
    if (theme.value === 'system') return systemTheme.value
    return theme.value
  })

  const isDark = computed(() => effectiveTheme.value === 'dark')

  // List of available background filenames (served from /backgrounds/)
  const availableBackgrounds = [
    // Will be populated dynamically or as filenames are added
  ]

  function setTheme(newTheme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme()
  }

  function setBackground(filename) {
    background.value = filename
    if (filename) {
      localStorage.setItem('background', filename)
    } else {
      localStorage.removeItem('background')
    }
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
    const el = document.getElementById('app-background')
    if (!el) return
    if (background.value) {
      el.style.backgroundImage = `url('/backgrounds/${background.value}')`
      el.style.backgroundSize = 'cover'
      el.style.backgroundPosition = 'center'
      el.style.backgroundAttachment = 'fixed'
    } else {
      el.style.backgroundImage = ''
    }
  }

  function initTheme() {
    if (!localStorage.getItem('theme')) {
      localStorage.setItem('theme', 'light')
      theme.value = 'light'
    }
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      systemTheme.value = e.matches ? 'dark' : 'light'
      if (theme.value === 'system') applyTheme()
    })
    applyTheme()
    // Apply background after DOM is ready
    setTimeout(applyBackground, 100)
  }

  watch(theme, applyTheme)

  return {
    theme,
    background,
    systemTheme,
    effectiveTheme,
    isDark,
    availableBackgrounds,
    setTheme,
    setBackground,
    initTheme,
    applyBackground,
  }
})
