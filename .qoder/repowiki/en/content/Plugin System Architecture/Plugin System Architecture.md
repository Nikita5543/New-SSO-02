# Plugin System Architecture

<cite>
**Referenced Files in This Document**
- [plugin_loader.py](file://backend/app/core/plugin_loader.py)
- [main.py](file://backend/app/main.py)
- [plugin.py](file://backend/app/plugins/accounting/plugin.py)
- [plugin.py](file://backend/app/plugins/configuration/plugin.py)
- [plugin.py](file://backend/app/plugins/incidents/plugin.py)
- [plugin.py](file://backend/app/plugins/inventory/plugin.py)
- [plugin.py](file://backend/app/plugins/performance/plugin.py)
- [plugin.py](file://backend/app/plugins/security_module/plugin.py)
- [endpoints.py](file://backend/app/plugins/accounting/endpoints.py)
- [endpoints.py](file://backend/app/plugins/configuration/endpoints.py)
- [endpoints.py](file://backend/app/plugins/incidents/endpoints.py)
- [pluginRegistry.js](file://frontend/src/stores/pluginRegistry.js)
- [main.js](file://frontend/src/main.js)
- [index.js](file://frontend/src/router/index.js)
- [IncidentsList.vue](file://frontend/src/plugins/incidents/views/IncidentsList.vue)
- [Accounting.vue](file://frontend/src/plugins/accounting/views/Accounting.vue)
- [Configuration.vue](file://frontend/src/plugins/configuration/views/Configuration.vue)
</cite>

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
10. [Appendices](#appendices)

## Introduction
This document describes the plugin-based system architecture of the platform. It explains how plugins are discovered, loaded, and registered in both the backend and frontend, and how they integrate with the main application. It also documents the standardized plugin structure, the plugin development lifecycle, and practical examples of plugin integration, menu generation, and state management. Communication patterns between the backend plugin loader and the frontend plugin registry are covered, along with extensibility mechanisms and best practices.

## Project Structure
The plugin system spans two primary areas:
- Backend: Dynamic discovery and registration of plugins via a loader that imports plugin modules and registers API routers under a plugin-specific prefix.
- Frontend: Runtime discovery of loaded plugins, dynamic registration of plugin manifests, and menu generation for navigation.

```mermaid
graph TB
subgraph "Backend"
A["FastAPI App<br/>main.py"]
B["Plugin Loader<br/>plugin_loader.py"]
C["Plugin Modules<br/>plugins/*/plugin.py"]
D["Plugin Routers<br/>plugins/*/endpoints.py"]
end
subgraph "Frontend"
E["Main Entry<br/>main.js"]
F["Plugin Registry Store<br/>pluginRegistry.js"]
G["Router & Views<br/>index.js + plugin views"]
end
A --> B
B --> C
C --> D
E --> F
E --> G
F --> G
```

**Diagram sources**
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [index.js:26-32](file://frontend/src/router/index.js#L26-L32)

**Section sources**
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [index.js:26-32](file://frontend/src/router/index.js#L26-L32)

## Core Components
- Backend plugin loader: Discovers plugin directories, validates plugin metadata and registration function, constructs a plugin context, and invokes the plugin’s register function to attach API routes.
- Plugin modules: Provide metadata and a register function that includes a FastAPI router under a plugin-scoped prefix.
- Plugin endpoints: Define API endpoints for each plugin’s domain logic.
- Frontend plugin registry: Dynamically loads plugin manifests from the backend, aggregates menu items, and exposes computed state for UI rendering.
- Frontend router and views: Define plugin routes and render plugin-specific views.

Key responsibilities:
- Backend: Plugin discovery, model registration, API router inclusion, and runtime plugin status exposure.
- Frontend: Plugin manifest registration, menu aggregation, route composition, and view rendering.

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [index.js:26-32](file://frontend/src/router/index.js#L26-L32)

## Architecture Overview
The system follows a dual-layer plugin architecture:
- Backend layer: Plugins are Python packages under a dedicated directory. Each plugin defines a metadata dictionary and a register function that receives a FastAPI app and a plugin context. The loader imports plugin models first, then the plugin module, validates metadata, and calls register to attach routes.
- Frontend layer: On startup, the frontend fetches the list of loaded plugins from the backend, constructs plugin manifests, and registers them in a Pinia store. Menu items are generated per plugin and exposed for the sidebar navigation.

```mermaid
sequenceDiagram
participant BE as "Backend App<br/>main.py"
participant Loader as "Plugin Loader<br/>plugin_loader.py"
participant Mod as "Plugin Module<br/>plugins/*/plugin.py"
participant Router as "Plugin Router<br/>plugins/*/endpoints.py"
participant FE as "Frontend Main<br/>main.js"
participant Reg as "Plugin Registry<br/>pluginRegistry.js"
BE->>Loader : "load_plugins(app)"
Loader->>Mod : "import plugin module"
Loader->>Loader : "validate PLUGIN_META and register()"
Loader->>BE : "include_router(prefix=context.api_prefix)"
FE->>BE : "GET /api/v1/plugins"
BE-->>FE : "loaded plugins list"
FE->>Reg : "registerPlugin(manifest)"
FE->>FE : "generate menu items per plugin"
```

**Diagram sources**
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

## Detailed Component Analysis

### Backend Plugin Loader
The loader performs:
- Directory scanning for plugin folders.
- Optional filtering by an enabled-plugins setting.
- Model import to register SQLAlchemy models with the shared metadata base.
- Plugin module import and validation of required metadata and registration function.
- Construction of a plugin context containing database base, API prefix, and security helpers.
- Invocation of the plugin’s register function to attach routes.
- Aggregation of plugin status and metadata for runtime reporting.

```mermaid
flowchart TD
Start(["Startup"]) --> Scan["Scan plugins directory"]
Scan --> Enabled{"Enabled list configured?"}
Enabled --> |Yes| Filter["Filter by enabled list"]
Enabled --> |No| Iterate["Iterate plugin folders"]
Filter --> Iterate
Iterate --> Validate["Check plugin.py presence"]
Validate --> ImportModels["Import plugin models (optional)"]
ImportModels --> ImportPlugin["Import plugin module"]
ImportPlugin --> CheckMeta{"Has PLUGIN_META and register()?"}
CheckMeta --> |No| Skip["Skip plugin with warning"]
CheckMeta --> |Yes| BuildCtx["Build PluginContext"]
BuildCtx --> CallRegister["Call register(app, context)"]
CallRegister --> AddInfo["Collect plugin info"]
Skip --> Next["Next plugin"]
AddInfo --> Next
Next --> Done(["Return loaded plugins"])
```

**Diagram sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [main.py:17-48](file://backend/app/main.py#L17-L48)

### Plugin Module Structure and Registration
Each plugin must provide:
- Metadata dictionary with at least name, version, description, and author.
- A register function that accepts the FastAPI app and a plugin context, and includes a router under a plugin-scoped prefix.

```mermaid
classDiagram
class PluginModule {
+PLUGIN_META
+register(app, context)
}
class PluginContext {
+db_base
+api_prefix
+get_db()
+get_current_user()
+get_current_admin_user()
}
class FastAPIApp {
+include_router(router, prefix, tags)
}
PluginModule --> PluginContext : "uses"
PluginModule --> FastAPIApp : "registers routes"
```

**Diagram sources**
- [plugin_loader.py:69-76](file://backend/app/core/plugin_loader.py#L69-L76)
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)

**Section sources**
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [plugin.py:1-17](file://backend/app/plugins/configuration/plugin.py#L1-L17)
- [plugin.py:1-17](file://backend/app/plugins/incidents/plugin.py#L1-L17)
- [plugin.py:1-17](file://backend/app/plugins/inventory/plugin.py#L1-L17)
- [plugin.py:1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [plugin.py:1-17](file://backend/app/plugins/security_module/plugin.py#L1-L17)

### Plugin Endpoints and API Exposure
Each plugin defines an API router with endpoints for its domain. The loader attaches each router under a prefix derived from the plugin’s metadata name. Authentication and authorization are enforced via dependency-injected security functions.

```mermaid
sequenceDiagram
participant Client as "Client"
participant Router as "Plugin Router<br/>endpoints.py"
participant DB as "Database Session"
participant Sec as "Security Dependencies"
Client->>Router : "HTTP Request"
Router->>Sec : "Depends(get_current_user/admin)"
Router->>DB : "Depends(get_db)"
Router-->>Client : "HTTP Response"
```

**Diagram sources**
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)
- [endpoints.py:1-71](file://backend/app/plugins/configuration/endpoints.py#L1-L71)
- [endpoints.py:1-122](file://backend/app/plugins/incidents/endpoints.py#L1-L122)

**Section sources**
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)
- [endpoints.py:1-71](file://backend/app/plugins/configuration/endpoints.py#L1-L71)
- [endpoints.py:1-122](file://backend/app/plugins/incidents/endpoints.py#L1-L122)

### Frontend Plugin Registry and Menu Generation
On startup, the frontend:
- Fetches the list of loaded plugins from the backend.
- Constructs plugin manifests with metadata and menu items.
- Registers each plugin in a Pinia store and marks initialization complete.
- Exposes computed lists of enabled plugins and aggregated menu items grouped by section and ordered by priority.

```mermaid
flowchart TD
FEStart["Frontend Startup"] --> Fetch["Fetch /api/v1/plugins"]
Fetch --> Parse["Parse loaded plugins"]
Parse --> Loop{"For each loaded plugin"}
Loop --> Manifest["Create manifest with metadata"]
Manifest --> Menu["Generate menu items"]
Menu --> Register["Register in pluginRegistry"]
Register --> Loop
Loop --> |Done| Init["Set initialized"]
Init --> Ready["UI ready with plugin menus"]
```

**Diagram sources**
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

**Section sources**
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

### Frontend Router Integration and View Rendering
The frontend router defines plugin routes and lazy-loads plugin views. Each plugin view consumes the backend APIs exposed under the plugin’s prefixed endpoints. The incidents view demonstrates fetching, creating, and updating incidents via authenticated fetch calls.

```mermaid
sequenceDiagram
participant Router as "Vue Router<br/>index.js"
participant View as "Plugin View<br/>IncidentsList.vue"
participant Auth as "Auth Store"
participant API as "Backend API<br/>/api/v1/plugins/incidents"
Router->>View : "Navigate to plugin route"
View->>Auth : "authFetch('/api/v1/plugins/incidents')"
Auth->>API : "Authenticated HTTP request"
API-->>Auth : "JSON response"
Auth-->>View : "Data"
View-->>Router : "Render UI"
```

**Diagram sources**
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)
- [IncidentsList.vue:41-104](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L104)

**Section sources**
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)
- [IncidentsList.vue:41-104](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L104)

### Practical Examples

#### Example: Incidents Plugin Integration
- Backend: The incidents plugin registers a router under a plugin-scoped prefix and exposes endpoints for listing, creating, retrieving, updating, and deleting incidents.
- Frontend: The incidents view fetches data from the backend, renders a list of incidents, supports creating new incidents, and updating statuses.

```mermaid
sequenceDiagram
participant FE as "IncidentsList.vue"
participant Auth as "Auth Store"
participant API as "Backend Incidents API"
FE->>Auth : "authFetch('/api/v1/plugins/incidents/')"
Auth->>API : "GET /api/v1/plugins/incidents/"
API-->>Auth : "200 OK + incidents"
Auth-->>FE : "JSON incidents"
FE->>Auth : "authFetch(..., POST ...)"
Auth->>API : "POST /api/v1/plugins/incidents/"
API-->>Auth : "200 OK + new incident"
Auth-->>FE : "Updated list"
```

**Diagram sources**
- [IncidentsList.vue:41-104](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L104)
- [endpoints.py:18-38](file://backend/app/plugins/incidents/endpoints.py#L18-L38)

**Section sources**
- [IncidentsList.vue:41-104](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L104)
- [endpoints.py:18-38](file://backend/app/plugins/incidents/endpoints.py#L18-L38)

#### Example: Menu Generation and Navigation
- The frontend generates menu items for each plugin and groups them by section and order. The router defines plugin routes that lazy-load plugin views.

```mermaid
flowchart LR
Menu["Menu Items (computed)"] --> Sidebar["Sidebar Navigation"]
Sidebar --> Routes["Router Routes"]
Routes --> Views["Plugin Views"]
```

**Diagram sources**
- [main.js:53-113](file://frontend/src/main.js#L53-L113)
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)

**Section sources**
- [main.js:53-113](file://frontend/src/main.js#L53-L113)
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)

#### Example: State Management with Plugin Registry
- The plugin registry maintains a reactive list of plugins, filters enabled ones, and computes aggregated menu items. It exposes getters to retrieve specific plugins and helpers to manage initialization.

```mermaid
classDiagram
class PluginRegistryStore {
+plugins : Ref~Array~
+initialized : Ref~boolean~
+enabledPlugins() : ComputedRef
+allMenuItems() : ComputedRef
+menuItemsBySection(section) : Function
+getPlugin(name) : Function
+registerPlugin(manifest) : void
+setInitialized() : void
}
```

**Diagram sources**
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

**Section sources**
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

## Dependency Analysis
The plugin system exhibits clear separation of concerns:
- Backend depends on the loader to discover and register plugins; each plugin depends on the loader-provided context to register routes.
- Frontend depends on the backend for plugin metadata and on the registry store for UI composition.
- Views depend on the router and the auth store for authenticated requests.

```mermaid
graph TB
Loader["plugin_loader.py"] --> App["main.py"]
Loader --> PM["plugins/*/plugin.py"]
PM --> PR["plugins/*/endpoints.py"]
FE_Main["frontend main.js"] --> FE_Reg["pluginRegistry.js"]
FE_Reg --> FE_Router["router/index.js"]
FE_Router --> FE_Views["plugin views"]
FE_Views --> Auth["auth store (implicit via authFetch)"]
```

**Diagram sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)

## Performance Considerations
- Plugin discovery scans the plugins directory and imports modules; keep the number of plugins reasonable and avoid heavy imports in plugin initialization.
- Route registration occurs during startup; minimize expensive operations inside register functions.
- Frontend plugin initialization fetches a small JSON payload; ensure the backend endpoint responds quickly.
- Lazy-loading of plugin views reduces initial bundle size; maintain this pattern for scalability.

## Troubleshooting Guide
Common issues and resolutions:
- Plugin not loaded: Verify the plugin folder contains a valid plugin module with metadata and a register function. Check backend logs for warnings or errors during discovery.
- Missing endpoints: Confirm the plugin’s register function includes the router with the correct prefix and tags.
- Frontend menu missing: Ensure the backend returns loaded plugins and the frontend’s manifest generation includes menu items for the plugin.
- Authentication failures: Verify that endpoints depend on appropriate security functions and that the frontend uses authenticated fetch calls.

**Section sources**
- [plugin_loader.py:89-97](file://backend/app/core/plugin_loader.py#L89-L97)
- [plugin.py:9-16](file://backend/app/plugins/accounting/plugin.py#L9-L16)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)

## Conclusion
The plugin system provides a clean, extensible architecture for both backend and frontend. The backend loader standardizes plugin discovery and registration, while the frontend registry enables dynamic UI composition and navigation. By adhering to the standardized plugin structure and leveraging the provided context and store utilities, developers can implement robust, maintainable plugins that integrate seamlessly with the main application.

## Appendices

### Standardized Plugin Structure
- Directory: backend/app/plugins/<plugin_name>/
- Required files:
  - plugin.py: Defines PLUGIN_META and a register(app, context) function.
  - endpoints.py: Defines APIRouter with plugin endpoints.
  - Optional: models.py and schemas.py for domain models and Pydantic schemas.

**Section sources**
- [plugin.py:1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [endpoints.py:1-61](file://backend/app/plugins/accounting/endpoints.py#L1-L61)

### Plugin Development Lifecycle
- Create plugin directory and files following the standardized structure.
- Implement endpoints and models/schemas as needed.
- Register routes in the plugin’s register function.
- Test endpoints via the backend API.
- On the frontend, add menu items and ensure routes are defined.
- Deploy backend and frontend together; verify plugin appears in the UI.

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [main.js:53-113](file://frontend/src/main.js#L53-L113)
- [index.js:114-144](file://frontend/src/router/index.js#L114-L144)

### Communication Patterns and Extensibility
- Backend-to-Frontend: The backend exposes a simple JSON endpoint listing loaded plugins. The frontend consumes this endpoint to build plugin manifests and menus.
- Data Sharing: Plugin views communicate with backend APIs using authenticated fetch calls, enabling secure data exchange.
- Extensibility: New plugins require minimal boilerplate—metadata, registration, and endpoints—allowing rapid feature addition.

**Section sources**
- [main.py:84-87](file://backend/app/main.py#L84-L87)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [IncidentsList.vue:41-104](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L104)