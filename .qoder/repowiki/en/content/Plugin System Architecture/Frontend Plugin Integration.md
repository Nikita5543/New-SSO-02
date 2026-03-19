# Frontend Plugin Integration

<cite>
**Referenced Files in This Document**
- [plugin_loader.py](file://backend/app/core/plugin_loader.py)
- [main.py](file://backend/app/main.py)
- [plugin.py (performance)](file://backend/app/plugins/performance/plugin.py)
- [endpoints.py (performance)](file://backend/app/plugins/performance/endpoints.py)
- [plugin.py (vlan)](file://backend/app/plugins/vlan/plugin.py)
- [endpoints.py (vlan)](file://backend/app/plugins/vlan/endpoints.py)
- [plugin.py (accounting)](file://backend/app/plugins/accounting/plugin.py)
- [plugin.py (configuration)](file://backend/app/plugins/configuration/plugin.py)
- [plugin.py (incidents)](file://backend/app/plugins/incidents/plugin.py)
- [plugin.py (inventory)](file://backend/app/plugins/inventory/plugin.py)
- [plugin.py (ipam)](file://backend/app/plugins/ipam/plugin.py)
- [plugin.py (security_module)](file://backend/app/plugins/security_module/plugin.py)
- [plugin.py (network_tools)](file://backend/app/plugins/network_tools/plugin.py)
- [endpoints.py (network_tools)](file://backend/app/plugins/network_tools/endpoints.py)
- [pluginRegistry.js](file://frontend/src/stores/pluginRegistry.js)
- [main.js](file://frontend/src/main.js)
- [index.js (router)](file://frontend/src/router/index.js)
- [Sidebar.vue](file://frontend/src/components/layout/Sidebar.vue)
- [SidebarItem.vue](file://frontend/src/components/layout/SidebarItem.vue)
- [DashboardLayout.vue](file://frontend/src/layouts/DashboardLayout.vue)
- [Performance.vue](file://frontend/src/plugins/performance/views/Performance.vue)
- [IncidentsList.vue](file://frontend/src/plugins/incidents/views/IncidentsList.vue)
- [Accounting.vue](file://frontend/src/plugins/accounting/views/Accounting.vue)
- [Ipam.vue](file://frontend/src/plugins/ipam/views/Ipam.vue)
- [Vlan.vue](file://frontend/src/plugins/vlan/views/Vlan.vue)
- [NetworkTools.vue](file://frontend/src/plugins/network_tools/views/NetworkTools.vue)
</cite>

## Update Summary
**Changes Made**
- Added comprehensive documentation for Network Tools plugin integration including routing, menu configuration, and Wrench icon implementation
- Updated frontend plugin registry configuration to include Network Tools plugin with proper Analytics section placement
- Enhanced router configuration documentation to cover Network Tools plugin lazy loading
- Added Network Tools plugin view implementation details with internal/external tool management
- Updated sidebar integration documentation to reflect Network Tools plugin menu item with Wrench icon
- Expanded plugin metadata consumption and UI component registration process documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)

## Introduction
This document explains how backend-loaded plugins are integrated into the frontend plugin registry, how dynamic components are loaded, and how routes are integrated. It documents the plugin registry store, plugin metadata consumption, and the UI component registration process. It also covers plugin-specific routing, lazy loading strategies, component composition patterns, and the communication between the frontend plugin registry and the backend plugin loader.

**Updated** The document now includes comprehensive coverage of the Network Tools plugin, which provides quick access to internal and external network resources with dedicated routing, menu configuration, and specialized tool management capabilities. The Network Tools plugin integrates seamlessly with the plugin registry system and follows the established patterns for plugin integration.

## Project Structure
The plugin integration spans two layers:
- Backend: A plugin loader discovers plugin packages, loads their metadata, and registers API routers under plugin-specific prefixes.
- Frontend: A plugin registry store is populated from backend plugin metadata, enabling dynamic UI menus and lazy-loaded routes.

```mermaid
graph TB
subgraph "Backend"
A["FastAPI App<br/>main.py"]
B["Plugin Loader<br/>plugin_loader.py"]
C["Plugin Modules<br/>plugins/*/plugin.py"]
D["Performance Plugin<br/>plugins/performance/plugin.py"]
E["Performance Endpoints<br/>plugins/performance/endpoints.py"]
F["VLAN Plugin<br/>plugins/vlan/plugin.py"]
G["VLAN Endpoints<br/>plugins/vlan/endpoints.py"]
H["Network Tools Plugin<br/>plugins/network_tools/plugin.py"]
I["Network Tools Endpoints<br/>plugins/network_tools/endpoints.py"]
end
subgraph "Frontend"
J["Plugin Registry Store<br/>pluginRegistry.js"]
K["App Initialization<br/>main.js"]
L["Router & Lazy Routes<br/>router/index.js"]
M["UI Layout & Menus<br/>Sidebar.vue"]
N["Plugin Views<br/>Performance.vue, IncidentsList.vue, Accounting.vue, Ipam.vue, Vlan.vue, NetworkTools.vue"]
O["Performance View<br/>Performance.vue"]
P["Network Tools View<br/>NetworkTools.vue"]
end
A --> B
B --> C
B --> D
D --> E
B --> F
F --> G
B --> H
H --> I
A --> |"GET /api/v1/plugins"| J
J --> K
K --> L
L --> M
M --> N
N --> O
N --> P
```

**Diagram sources**
- [main.py:17-87](file://backend/app/main.py#L17-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py (performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [endpoints.py (performance):265-300](file://backend/app/plugins/performance/endpoints.py#L265-L300)
- [plugin.py (vlan):1-17](file://backend/app/plugins/vlan/plugin.py#L1-L17)
- [endpoints.py (vlan):1-221](file://backend/app/plugins/vlan/endpoints.py#L1-L221)
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)
- [Performance.vue:1-488](file://frontend/src/plugins/performance/views/Performance.vue#L1-L488)
- [NetworkTools.vue:1-180](file://frontend/src/plugins/network_tools/views/NetworkTools.vue#L1-L180)

**Section sources**
- [main.py:17-87](file://backend/app/main.py#L17-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)

## Core Components
- Backend plugin loader: Discovers plugin directories, imports plugin modules, reads metadata, and registers API routers with plugin-specific prefixes.
- Backend plugin modules: Provide metadata and a registration function to attach routes to the FastAPI app.
- Frontend plugin registry store: Holds plugin manifests, exposes computed menu items, and tracks initialization state.
- Frontend app initialization: Fetches backend plugin list, constructs plugin manifests, and registers them in the store.
- Frontend router: Defines lazy-loaded routes for plugin views and integrates them into the application layout.
- Frontend UI layout: Renders plugin menu items grouped by sections and orders, integrating with the router.

**Updated** The system now includes comprehensive support for the Network Tools plugin, which provides quick access to internal and external network resources with dedicated routing, menu configuration, and specialized tool management capabilities. The Network Tools plugin integrates seamlessly with the plugin registry system and follows established patterns for plugin integration.

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py (performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [endpoints.py (performance):265-300](file://backend/app/plugins/performance/endpoints.py#L265-L300)
- [plugin.py (vlan):1-17](file://backend/app/plugins/vlan/plugin.py#L1-L17)
- [endpoints.py (vlan):1-221](file://backend/app/plugins/vlan/endpoints.py#L1-L221)
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)

## Architecture Overview
The integration follows a clear pipeline:
- Backend startup loads plugins and exposes a list endpoint.
- Frontend initializes by fetching the plugin list and registering plugin manifests.
- Frontend router lazily loads plugin views and renders them within the dashboard layout.
- Frontend UI composes plugin menu items from the registry into categorized sections.

```mermaid
sequenceDiagram
participant BE as "Backend App<br/>main.py"
participant PL as "Plugin Loader<br/>plugin_loader.py"
participant PM as "Plugin Modules<br/>plugins/*/plugin.py"
participant PERF as "Performance Plugin<br/>plugins/performance/plugin.py"
participant EP as "Performance Endpoints<br/>plugins/performance/endpoints.py"
participant NT as "Network Tools Plugin<br/>plugins/network_tools/plugin.py"
participant NTE as "Network Tools Endpoints<br/>plugins/network_tools/endpoints.py"
participant FE as "Frontend App<br/>main.js"
participant PR as "Plugin Registry<br/>pluginRegistry.js"
participant RT as "Router<br/>router/index.js"
participant UI as "UI Layout<br/>Sidebar.vue"
BE->>PL : "Startup lifecycle"
PL->>PM : "Import plugin modules"
PL->>PERF : "Import Performance plugin"
PERF->>EP : "Include router with API prefix"
EP-->>PERF : "Registered endpoints"
PL->>NT : "Import Network Tools plugin"
NT->>NTE : "Include router with API prefix"
NTE-->>NT : "Registered endpoints"
PM-->>PL : "PLUGIN_META, register()"
PL->>BE : "include_router(prefix=/api/v1/plugins/{name})"
BE-->>FE : "GET /api/v1/plugins"
FE->>PR : "registerPlugin(manifest)"
PR-->>UI : "enabledPlugins, menuItemsBySection()"
RT-->>FE : "Lazy route to plugin view"
UI-->>RT : "Render plugin menu items"
```

**Diagram sources**
- [main.py:17-87](file://backend/app/main.py#L17-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py (performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [endpoints.py (performance):265-300](file://backend/app/plugins/performance/endpoints.py#L265-L300)
- [plugin.py (vlan):1-17](file://backend/app/plugins/vlan/plugin.py#L1-L17)
- [endpoints.py (vlan):1-221](file://backend/app/plugins/vlan/endpoints.py#L1-L221)
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)

## Detailed Component Analysis

### Backend Plugin Loader and Registration
- Discovery: Iterates plugin directories, filters by enabled list, and imports plugin modules.
- Metadata and registration: Reads PLUGIN_META and invokes register(app, context) to attach routers with a plugin-specific prefix.
- API prefix: Uses a structured prefix derived from plugin name to avoid conflicts.
- Error handling: Logs failures and records plugin status.

```mermaid
flowchart TD
Start(["Startup"]) --> Scan["Scan plugins directory"]
Scan --> Enabled{"Enabled in settings?"}
Enabled --> |No| Skip["Skip plugin"]
Enabled --> |Yes| ImportModels["Import plugin models"]
ImportModels --> ImportPlugin["Import plugin module"]
ImportPlugin --> CheckMeta{"Has PLUGIN_META and register()?"}
CheckMeta --> |No| Warn["Log warning and skip"]
CheckMeta --> |Yes| BuildCtx["Build PluginContext"]
BuildCtx --> Register["Call register(app, context)"]
Register --> AddInfo["Collect plugin info"]
AddInfo --> Done(["Loaded"])
Warn --> Done
Skip --> Done
```

**Diagram sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py (performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [endpoints.py (performance):265-300](file://backend/app/plugins/performance/endpoints.py#L265-L300)
- [plugin.py (vlan):1-17](file://backend/app/plugins/vlan/plugin.py#L1-L17)
- [endpoints.py (vlan):1-221](file://backend/app/plugins/vlan/endpoints.py#L1-L221)
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)

### Network Tools Plugin Backend Implementation
The Network Tools plugin provides quick access to internal and external network resources with two main API endpoints:

- **Internal Tools**: Access to internal network management systems including NetBox (IPAM and DCIM), LibreNMS (network monitoring), ServiceBase (service management), Zabbix (infrastructure monitoring), Wiki-NOC (documentation), Jira-SPD (project management), Grafana (dashboards), and Looking Glass (LG)
- **External Tools**: Access to external network resources including RIPE Database (WHOIS) and ICANN Whois lookup

```mermaid
classDiagram
class NetworkToolsPlugin {
+PLUGIN_META : Object
+register(app, context) : Function
}
class NetworkToolsEndpoints {
+internal_tools : Array
+external_tools : Array
+get_internal_tools() : Endpoint
+get_external_tools() : Endpoint
}
NetworkToolsPlugin --> NetworkToolsEndpoints : "includes router"
```

**Diagram sources**
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)

**Section sources**
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)

### Frontend Plugin Registry Store
- Responsibilities: Stores plugin manifests, computes enabled plugins, aggregates menu items, filters by section, and exposes getters.
- Computed aggregations: enabledPlugins, allMenuItems, and menuItemsBySection enable UI composition.
- Idempotent registration: Prevents duplicates and warns on invalid manifests.

```mermaid
classDiagram
class PluginRegistryStore {
+plugins : Ref~Array~
+initialized : Ref~boolean~
+enabledPlugins() : ComputedRef~Array~
+allMenuItems() : ComputedRef~Array~
+menuItemsBySection(section) : Function
+getPlugin(name) : Function
+registerPlugin(manifest) : Function
+setInitialized() : Function
}
```

**Diagram sources**
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

**Section sources**
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

### Frontend App Initialization and Plugin Manifest Construction
- Fetching plugin list: Calls the backend list endpoint during app bootstrap.
- Manifest creation: Builds a manifest per plugin with label, version, description, enabled flag, and menu items.
- Menu item mapping: Provides icons, paths, sections, and ordering for each plugin.
- Initialization flag: Marks registry as ready after successful population.

**Updated** The Network Tools plugin is now included in the menu configuration with proper section assignment and ordering in the Analytics section, positioned alongside other monitoring tools with the Wrench icon.

```mermaid
sequenceDiagram
participant Init as "initApp(main.js)"
participant Fetch as "fetch('/api/v1/plugins')"
participant Reg as "usePluginRegistryStore()"
participant Menu as "getMenuItemsForPlugin()"
Init->>Fetch : "GET /api/v1/plugins"
Fetch-->>Init : "Array of plugin info (including Network Tools)"
Init->>Reg : "registerPlugin(manifest)"
Reg-->>Init : "Store populated"
Init->>Menu : "Map plugin names to menu items (Network Tools)"
Menu-->>Init : "Wrench icon, path, section, order"
Init->>Reg : "setInitialized()"
```

**Diagram sources**
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

**Section sources**
- [main.js:18-164](file://frontend/src/main.js#L18-L164)

### Frontend Router and Dynamic Component Loading
- Lazy routes: Uses dynamic imports for plugin views to achieve code-splitting and lazy loading.
- Route hierarchy: Nested under the dashboard layout with plugin-specific paths.
- Composition: Integrates with the layout and auth guards.

**Updated** The router now includes the Network Tools plugin route with proper lazy loading configuration alongside other monitoring and analytics plugins, using the path `/plugins/network-tools`.

```mermaid
flowchart TD
Entry(["App Entry"]) --> LoadRouter["Load router/index.js"]
LoadRouter --> DefineRoutes["Define routes with lazy components"]
DefineRoutes --> AddNetworkTools["Add Network Tools route: /plugins/network-tools"]
AddNetworkTools --> Guard["Apply beforeEach guards"]
Guard --> Render["Render DashboardLayout with RouterView"]
Render --> Lazy["On navigation, load plugin view via dynamic import"]
```

**Diagram sources**
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [DashboardLayout.vue:1-125](file://frontend/src/layouts/DashboardLayout.vue#L1-L125)

**Section sources**
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [DashboardLayout.vue:1-125](file://frontend/src/layouts/DashboardLayout.vue#L1-L125)

### UI Component Registration and Menu Composition
- Sidebar sections: Groups core and plugin items into sections (General, Operations, Analytics, Security, Admin, Pages, Other).
- Ordering: Sorts items by order field within each section.
- Visibility: Respects role-based visibility checks.
- Icons and links: Uses Lucide icons and router links for navigation.

**Updated** The Network Tools plugin is now integrated into the Analytics section with proper ordering and Wrench icon selection, positioned alongside other monitoring and analytics tools.

```mermaid
classDiagram
class Sidebar {
+coreGeneralItems : Array
+corePageItems : ComputedRef
+coreOtherItems : Array
+operationsPluginItems : ComputedRef
+analyticsPluginItems : ComputedRef
+securityPluginItems : ComputedRef
+adminPluginItems : ComputedRef
+generalItems() : ComputedRef
+pageItems() : ComputedRef
+otherItems() : ComputedRef
+isItemVisible(item) : Function
}
class SidebarItem {
+item : Object
+isSubItem : Boolean
+isActive : ComputedRef
+hasChildren : ComputedRef
}
Sidebar --> SidebarItem : "renders"
```

**Diagram sources**
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)
- [SidebarItem.vue:1-74](file://frontend/src/components/layout/SidebarItem.vue#L1-L74)

**Section sources**
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)
- [SidebarItem.vue:1-74](file://frontend/src/components/layout/SidebarItem.vue#L1-L74)

### Plugin-Specific View Implementation Examples
- Performance view: Comprehensive system monitoring dashboard with real-time metrics, container status, alarms, and plugin statistics.
- Incidents list view: Demonstrates state management, API integration via auth store, CRUD actions, and UI composition with badges and forms.
- Accounting view: Minimal example showcasing a card-based layout and placeholder content.
- **IPAM view**: Comprehensive IP address management interface with validation, change application, and database querying capabilities.
- **VLAN view**: Advanced network management interface with VLAN discovery, statistics visualization, and database interaction capabilities.
- **Network Tools view**: Comprehensive tool management interface with tabbed navigation for internal and external tools, dynamic icon mapping, and external link handling.

**Updated** Added detailed documentation for the Network Tools plugin view implementation, which provides quick access to internal and external network resources. The Network Tools view includes tabbed navigation for internal and external tools, dynamic icon mapping based on tool names, and external link handling with proper security attributes.

```mermaid
sequenceDiagram
participant View as "NetworkTools.vue"
participant Auth as "useAuthStore()"
participant API as "Backend API"
participant UI as "Vue Components"
View->>Auth : "authFetch('/api/v1/plugins/network_tools/internal-tools')"
Auth->>API : "HTTP GET /internal-tools"
API-->>Auth : "Internal tools list"
Auth-->>View : "Response with tools array"
View->>Auth : "authFetch('/api/v1/plugins/network_tools/external-tools')"
Auth->>API : "HTTP GET /external-tools"
API-->>Auth : "External tools list"
Auth-->>View : "Response"
View->>UI : "Render tool cards with icons"
View->>UI : "Handle external link clicks"
```

**Diagram sources**
- [NetworkTools.vue:67-126](file://frontend/src/plugins/network_tools/views/NetworkTools.vue#L67-L126)

**Section sources**
- [Performance.vue:1-488](file://frontend/src/plugins/performance/views/Performance.vue#L1-L488)
- [IncidentsList.vue:1-268](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L1-L268)
- [Accounting.vue:1-34](file://frontend/src/plugins/accounting/views/Accounting.vue#L1-L34)
- [Ipam.vue:1-489](file://frontend/src/plugins/ipam/views/Ipam.vue#L1-L489)
- [Vlan.vue:1-200](file://frontend/src/plugins/vlan/views/Vlan.vue#L1-L200)
- [NetworkTools.vue:1-180](file://frontend/src/plugins/network_tools/views/NetworkTools.vue#L1-L180)

### Communication Between Frontend Plugin Registry and Backend Plugin Loader
- Backend exposes a list endpoint returning loaded plugin metadata with status.
- Frontend initializes by fetching this endpoint, constructing manifests, and registering them in the store.
- Menu items are mapped based on plugin names and grouped into sections.

**Updated** The communication now includes the Network Tools plugin metadata and menu item configuration, providing seamless integration with the centralized monitoring ecosystem alongside other plugins.

```mermaid
sequenceDiagram
participant FE as "Frontend main.js"
participant BE as "Backend main.py"
participant PL as "plugin_loader.py"
FE->>BE : "GET /api/v1/plugins"
BE->>PL : "Access app.state.loaded_plugins"
PL-->>BE : "List of plugin info (including Network Tools)"
BE-->>FE : "JSON array (with Network Tools plugin)"
FE->>FE : "Construct manifests and menu items (Network Tools)"
FE->>FE : "registerPlugin(manifest) for Network Tools"
```

**Diagram sources**
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [main.py:84-87](file://backend/app/main.py#L84-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)

**Section sources**
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [main.py:84-87](file://backend/app/main.py#L84-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)

## Dependency Analysis
- Backend depends on plugin modules for metadata and registration functions.
- Frontend depends on backend for plugin metadata and on the router for navigation.
- UI layout depends on the plugin registry store for menu composition.

**Updated** Dependencies now include the Network Tools plugin integration across all layers, providing comprehensive tool management capabilities alongside the existing Performance, VLAN, and other plugin integrations.

```mermaid
graph LR
BE_Main["backend/main.py"] --> BE_Loader["backend/core/plugin_loader.py"]
BE_Loader --> BE_Plugin["backend/plugins/*/plugin.py"]
BE_Loader --> BE_Perf["backend/plugins/performance/plugin.py"]
BE_Loader --> BE_VLAN["backend/plugins/vlan/plugin.py"]
BE_Loader --> BE_NT["backend/plugins/network_tools/plugin.py"]
BE_Perf --> BE_Endpoints["backend/plugins/performance/endpoints.py"]
BE_VLAN --> BE_VLAN_Endpoints["backend/plugins/vlan/endpoints.py"]
BE_NT --> BE_NT_Endpoints["backend/plugins/network_tools/endpoints.py"]
FE_Init["frontend/src/main.js"] --> FE_Registry["frontend/src/stores/pluginRegistry.js"]
FE_Registry --> FE_Sidebar["frontend/src/components/layout/Sidebar.vue"]
FE_Router["frontend/src/router/index.js"] --> FE_VIEWS["frontend/src/plugins/*/views/*.vue"]
FE_Router --> FE_PERF_View["frontend/src/plugins/performance/views/Performance.vue"]
FE_Router --> FE_NT_View["frontend/src/plugins/network_tools/views/NetworkTools.vue"]
FE_Sidebar --> FE_Router
```

**Diagram sources**
- [main.py:17-87](file://backend/app/main.py#L17-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py (performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [endpoints.py (performance):265-300](file://backend/app/plugins/performance/endpoints.py#L265-L300)
- [plugin.py (vlan):1-17](file://backend/app/plugins/vlan/plugin.py#L1-L17)
- [endpoints.py (vlan):1-221](file://backend/app/plugins/vlan/endpoints.py#L1-L221)
- [plugin.py (network_tools):1-18](file://backend/app/plugins/network_tools/plugin.py#L1-L18)
- [endpoints.py (network_tools):1-42](file://backend/app/plugins/network_tools/endpoints.py#L1-L42)
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)

**Section sources**
- [main.py:17-87](file://backend/app/main.py#L17-L87)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)

## Performance Considerations
- Lazy loading: Dynamic imports in router reduce initial bundle size and improve perceived load time.
- Conditional rendering: Sidebar sections are only rendered when plugin items exist.
- Computed properties: Aggregations minimize recomputation and keep UI reactive efficiently.
- Backend filtering: Enabling only required plugins reduces startup overhead.
- **Performance optimization**: The Network Tools plugin uses efficient data fetching with concurrent API calls and proper loading state management.

**Updated** Performance considerations now include the Network Tools plugin's efficient data fetching strategies and concurrent API calls for internal and external tools.

## Troubleshooting Guide
- Plugin not appearing in UI:
  - Verify backend plugin status is loaded and returned by the list endpoint.
  - Confirm frontend registerPlugin is invoked and initialized flag is set.
- Incorrect menu grouping or ordering:
  - Check section labels and order fields in the frontend menu mapping.
- Route not loading:
  - Ensure lazy route path matches the plugin view path and component resolves.
- Authentication gating:
  - Confirm router guards align with required roles and auth store state.
- **Network Tools plugin specific issues**:
  - Verify `/api/v1/plugins/network_tools` endpoint is accessible and returns expected tool lists.
  - Check that the Network Tools view component properly handles loading states and error conditions.
  - Ensure proper authentication for Network Tools API endpoints.
  - Validate that internal and external tool configurations are correctly formatted.
  - Check that external tool URLs are accessible and properly handled with security attributes.
  - Verify that tool icon mapping works correctly for all configured tools.

**Updated** Added troubleshooting guidance specifically for Network Tools plugin integration issues, including tool management specific problems.

**Section sources**
- [main.js:18-164](file://frontend/src/main.js#L18-L164)
- [index.js (router):1-192](file://frontend/src/router/index.js#L1-L192)
- [Sidebar.vue:1-291](file://frontend/src/components/layout/Sidebar.vue#L1-L291)

## Conclusion
The frontend plugin integration leverages a clean separation of concerns: backend plugins expose metadata and API routes, while the frontend consumes this information to build a dynamic registry, lazy-load views, and compose a responsive UI. This approach supports scalable plugin development, maintainable navigation, and efficient runtime performance.

**Updated** The system now includes comprehensive plugin integration capabilities with the addition of the Network Tools plugin, which provides quick access to internal and external network resources. The Network Tools plugin demonstrates advanced plugin integration patterns with sophisticated state management, real-time tool access, and comprehensive resource management functionality. This expanded plugin ecosystem enhances the platform's operational capabilities while maintaining the flexibility of the plugin architecture across all operational and administrative domains.