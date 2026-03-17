import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref(localStorage.getItem('theme') || 'light')
  const systemTheme = ref(
    window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  )

  const effectiveTheme = computed(() => {
    if (theme.value === 'system') return systemTheme.value
    return theme.value
  })

  const isDark = computed(() => effectiveTheme.value === 'dark')

  function setTheme(newTheme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme()
  }

  function applyTheme() {
    const root = document.documentElement
    if (effectiveTheme.value === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }

  function initTheme() {
    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      systemTheme.value = e.matches ? 'dark' : 'light'
      if (theme.value === 'system') applyTheme()
    })
    applyTheme()
  }

  watch(theme, applyTheme)

  return {
    theme,
    systemTheme,
    effectiveTheme,
    isDark,
    setTheme,
    initTheme,
  }
})
