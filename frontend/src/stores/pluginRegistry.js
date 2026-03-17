import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const usePluginRegistryStore = defineStore('pluginRegistry', () => {
  const plugins = ref([])
  const initialized = ref(false)

  const enabledPlugins = computed(() =>
    plugins.value.filter((p) => p.enabled !== false)
  )

  const allMenuItems = computed(() =>
    enabledPlugins.value.flatMap((p) => p.menuItems || [])
  )

  function menuItemsBySection(section = 'general') {
    return allMenuItems.value
      .filter((item) => (item.section || 'general') === section)
      .sort((a, b) => (a.order || 0) - (b.order || 0))
  }

  function getPlugin(name) {
    return plugins.value.find((p) => p.name === name)
  }

  function registerPlugin(manifest) {
    if (!manifest || !manifest.name) {
      console.warn('Invalid plugin manifest:', manifest)
      return
    }
    if (plugins.value.find((p) => p.name === manifest.name)) {
      console.warn(`Plugin '${manifest.name}' already registered`)
      return
    }
    plugins.value.push(manifest)
  }

  function setInitialized() {
    initialized.value = true
  }

  return {
    plugins,
    initialized,
    enabledPlugins,
    allMenuItems,
    menuItemsBySection,
    getPlugin,
    registerPlugin,
    setInitialized,
  }
})
