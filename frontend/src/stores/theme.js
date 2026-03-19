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
  const hasBackground = computed(() => !!background.value)

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
    setTimeout(applyBackground, 50)
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
  }
})
