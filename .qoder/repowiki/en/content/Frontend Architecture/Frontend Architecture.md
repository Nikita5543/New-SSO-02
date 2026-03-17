# Frontend Architecture

<cite>
**Referenced Files in This Document**
- [main.js](file://frontend/src/main.js)
- [App.vue](file://frontend/src/App.vue)
- [router/index.js](file://frontend/src/router/index.js)
- [stores/auth.js](file://frontend/src/stores/auth.js)
- [stores/pluginRegistry.js](file://frontend/src/stores/pluginRegistry.js)
- [stores/theme.js](file://frontend/src/stores/theme.js)
- [layouts/DashboardLayout.vue](file://frontend/src/layouts/DashboardLayout.vue)
- [components/layout/Sidebar.vue](file://frontend/src/components/layout/Sidebar.vue)
- [components/layout/SidebarItem.vue](file://frontend/src/components/layout/SidebarItem.vue)
- [components/ui/Button.vue](file://frontend/src/components/ui/Button.vue)
- [components/ui/ThemeToggle.vue](file://frontend/src/components/ui/ThemeToggle.vue)
- [plugins/incidents/views/IncidentsList.vue](file://frontend/src/plugins/incidents/views/IncidentsList.vue)
- [assets/css/main.css](file://frontend/src/assets/css/main.css)
- [lib/utils.js](file://frontend/src/lib/utils.js)
- [tailwind.config.js](file://frontend/tailwind.config.js)
- [vite.config.cjs](file://frontend/vite.config.cjs)
- [package.json](file://frontend/package.json)
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
This document describes the frontend architecture of the Vue 3 application. It covers the component-based architecture, state management with Pinia, routing with Vue Router, and the plugin registry system. It also documents the layout system, reusable UI components, integration with backend APIs, component hierarchy, data flow patterns, and communication between the frontend and backend. Additional topics include the plugin view integration system, dynamic component loading, theme management, responsive design principles, accessibility considerations, and performance optimization strategies.

## Project Structure
The frontend is organized around a clear separation of concerns:
- Application bootstrap and initialization in main.js
- Root component rendering via App.vue
- Routing configuration and navigation guards in router/index.js
- Feature-specific views under views/
- Layout components under layouts/
- Reusable UI components under components/ui/
- Plugin-specific views under plugins/<plugin>/views/
- State management stores under stores/
- Utility helpers under lib/
- Styling via Tailwind CSS and global CSS

```mermaid
graph TB
subgraph "Bootstrap"
MJS["main.js"]
APP["App.vue"]
end
subgraph "Routing"
ROUTER["router/index.js"]
end
subgraph "Layout"
DL["layouts/DashboardLayout.vue"]
SB["components/layout/Sidebar.vue"]
SBI["components/layout/SidebarItem.vue"]
end
subgraph "UI Components"
BTN["components/ui/Button.vue"]
TT["components/ui/ThemeToggle.vue"]
end
subgraph "Stores"
AUTH["stores/auth.js"]
REG["stores/pluginRegistry.js"]
THEME["stores/theme.js"]
end
subgraph "Views"
INC["plugins/incidents/views/IncidentsList.vue"]
end
MJS --> APP
MJS --> ROUTER
MJS --> AUTH
MJS --> REG
APP --> ROUTER
ROUTER --> DL
DL --> SB
SB --> SBI
DL --> BTN
DL --> TT
SB --> REG
DL --> AUTH
INC --> AUTH
```

**Diagram sources**
- [main.js:1-132](file://frontend/src/main.js#L1-L132)
- [App.vue:1-17](file://frontend/src/App.vue#L1-L17)
- [router/index.js:1-174](file://frontend/src/router/index.js#L1-L174)
- [layouts/DashboardLayout.vue:1-125](file://frontend/src/layouts/DashboardLayout.vue#L1-L125)
- [components/layout/Sidebar.vue:1-258](file://frontend/src/components/layout/Sidebar.vue#L1-L258)
- [components/layout/SidebarItem.vue:1-74](file://frontend/src/components/layout/SidebarItem.vue#L1-L74)
- [components/ui/Button.vue:1-66](file://frontend/src/components/ui/Button.vue#L1-L66)
- [components/ui/ThemeToggle.vue:1-36](file://frontend/src/components/ui/ThemeToggle.vue#L1-L36)
- [stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)
- [stores/pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [stores/theme.js:1-53](file://frontend/src/stores/theme.js#L1-L53)
- [plugins/incidents/views/IncidentsList.vue:1-268](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L1-L268)

**Section sources**
- [main.js:1-132](file://frontend/src/main.js#L1-L132)
- [router/index.js:1-174](file://frontend/src/router/index.js#L1-L174)

## Core Components
- Application bootstrap initializes Pinia, Vue Router, and performs pre-mount tasks:
  - Initializes authentication state by restoring tokens and fetching user profile
  - Dynamically loads plugin metadata from the backend and registers them
  - Mounts the root application
- Root component renders the active route via RouterView
- Router defines core routes, nested settings routes, help pages, and plugin routes with lazy loading
- Stores:
  - Authentication store manages tokens, roles, and secure fetches
  - Plugin registry aggregates plugin manifests and menu items
  - Theme store manages light/dark/system themes and applies CSS classes

Key responsibilities:
- main.js orchestrates initialization and plugin registration
- router/index.js controls navigation and guards
- stores provide centralized state for auth, plugins, and theme
- views and components consume stores and render UI

**Section sources**
- [main.js:1-132](file://frontend/src/main.js#L1-L132)
- [App.vue:1-17](file://frontend/src/App.vue#L1-L17)
- [router/index.js:1-174](file://frontend/src/router/index.js#L1-L174)
- [stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)
- [stores/pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [stores/theme.js:1-53](file://frontend/src/stores/theme.js#L1-L53)

## Architecture Overview
The frontend follows a layered architecture:
- Presentation Layer: Views and components
- Layout Layer: DashboardLayout and Sidebar
- State Management: Pinia stores
- Routing: Vue Router with lazy-loaded plugin routes
- Styling: Tailwind CSS with CSS custom properties and dark mode support
- Backend Integration: REST endpoints accessed via fetch wrappers

```mermaid
graph TB
subgraph "Presentation"
VIEWS["Views (Dashboard, Settings, Help, Plugins)"]
UI["UI Components (Button, Card, Input, Dropdown, etc.)"]
end
subgraph "Layout"
DL["DashboardLayout"]
SB["Sidebar"]
end
subgraph "State"
AUTH["Auth Store"]
REG["Plugin Registry Store"]
THEME["Theme Store"]
end
subgraph "Routing"
ROUTER["Vue Router"]
end
subgraph "Styling"
CSS["Tailwind CSS + main.css"]
end
subgraph "Backend"
API["/api/v1/* endpoints"]
end
DL --> SB
DL --> VIEWS
VIEWS --> UI
VIEWS --> AUTH
SB --> REG
DL --> THEME
ROUTER --> VIEWS
VIEWS --> API
AUTH --> API
CSS --> UI
CSS --> DL
```

**Diagram sources**
- [layouts/DashboardLayout.vue:1-125](file://frontend/src/layouts/DashboardLayout.vue#L1-L125)
- [components/layout/Sidebar.vue:1-258](file://frontend/src/components/layout/Sidebar.vue#L1-L258)
- [router/index.js:1-174](file://frontend/src/router/index.js#L1-L174)
- [stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)
- [stores/pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [stores/theme.js:1-53](file://frontend/src/stores/theme.js#L1-L53)
- [assets/css/main.css:1-77](file://frontend/src/assets/css/main.css#L1-L77)
- [plugins/incidents/views/IncidentsList.vue:1-268](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L1-L268)

## Detailed Component Analysis

### Authentication and Session Management
The authentication store encapsulates:
- Token lifecycle (access/refresh), expiry checks, and persistence
- Role-based access (admin/user)
- Secure fetch wrapper that automatically retries on 401 with token refresh
- Logout with backend cleanup

```mermaid
sequenceDiagram
participant U as "User"
participant C as "Component"
participant AS as "Auth Store"
participant BE as "Backend API"
U->>C : "Submit login form"
C->>AS : "login(credentials)"
AS->>BE : "POST /api/v1/auth/login"
BE-->>AS : "200 {access_token, refresh_token, user}"
AS->>AS : "Persist tokens and expiry"
AS-->>C : "Success"
C->>BE : "Protected request"
BE-->>C : "401 Unauthorized"
C->>AS : "authFetch(url)"
AS->>BE : "POST /api/v1/auth/refresh"
BE-->>AS : "200 {new tokens}"
AS->>BE : "Retry original request"
BE-->>AS : "200 Success"
AS-->>C : "Response"
```

**Diagram sources**
- [stores/auth.js:29-197](file://frontend/src/stores/auth.js#L29-L197)

**Section sources**
- [stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)

### Plugin Registry and Dynamic Menu
The plugin registry:
- Registers plugin manifests with metadata and menu items
- Exposes computed aggregations (enabled plugins, menu items by section)
- Provides lookup and initialization state

Dynamic plugin loading:
- On startup, main.js fetches plugin list from backend
- For each loaded plugin, constructs a manifest and registers it
- Menu items are injected into the sidebar by section

```mermaid
flowchart TD
Start(["App Initialization"]) --> Fetch["Fetch /api/v1/plugins"]
Fetch --> Parse["Parse plugin list"]
Parse --> Loop{"For each plugin"}
Loop --> |status=loaded| Register["Create manifest<br/>registerPlugin(manifest)"]
Loop --> |otherwise| Skip["Skip"]
Register --> Next["Next plugin"]
Skip --> Next
Next --> Done{"All processed?"}
Done --> |No| Loop
Done --> SetInit["setInitialized()"]
SetInit --> End(["Ready"])
```

**Diagram sources**
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [stores/pluginRegistry.js:26-40](file://frontend/src/stores/pluginRegistry.js#L26-L40)

**Section sources**
- [main.js:18-132](file://frontend/src/main.js#L18-L132)
- [stores/pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

### Routing and Navigation Guards
Router configuration:
- Lazy loads plugin views using dynamic imports
- Defines nested routes for settings and children redirection
- Enforces guards:
  - requiresAuth for protected areas
  - guest for auth pages when already logged in
  - requiresAdmin for admin-only routes

```mermaid
flowchart TD
Enter(["Route Change"]) --> CheckGuest{"to.meta.guest?"}
CheckGuest --> |Yes & Authenticated| RedirectHome["next('/dashboard')"]
CheckGuest --> |No| CheckAuth{"to.meta.requiresAuth?"}
CheckAuth --> |Yes & Not Authenticated| RedirectSignIn["next('/auth/signin')"]
CheckAuth --> |No| CheckAdmin{"to.meta.requiresAdmin?"}
CheckAdmin --> |Yes & Not Admin| RedirectDash["next('/dashboard')"]
CheckAdmin --> |No| Proceed["next()"]
```

**Diagram sources**
- [router/index.js:159-171](file://frontend/src/router/index.js#L159-L171)

**Section sources**
- [router/index.js:1-174](file://frontend/src/router/index.js#L1-L174)

### Layout System and Sidebar
DashboardLayout coordinates:
- Desktop sidebar and mobile overlay/slide
- Header with theme toggle and user dropdown
- Main content area via RouterView

Sidebar composes:
- Core items (Dashboard, Users for admins, Settings, Help)
- Plugin sections (Operations, Analytics, Security, Admin, Pages, Other)
- Visibility controlled by roles and computed aggregations from plugin registry
- Collapsible groups for parent items with children

```mermaid
classDiagram
class DashboardLayout {
+sidebarOpen : boolean
+handleLogout()
}
class Sidebar {
+coreGeneralItems
+corePageItems
+coreOtherItems
+menuItemsBySection(section)
+isItemVisible(item)
}
class SidebarItem {
+item : Object
+isSubItem : boolean
+isActive
+hasChildren
}
DashboardLayout --> Sidebar : "renders"
Sidebar --> SidebarItem : "iterates"
```

**Diagram sources**
- [layouts/DashboardLayout.vue:1-125](file://frontend/src/layouts/DashboardLayout.vue#L1-L125)
- [components/layout/Sidebar.vue:1-258](file://frontend/src/components/layout/Sidebar.vue#L1-L258)
- [components/layout/SidebarItem.vue:1-74](file://frontend/src/components/layout/SidebarItem.vue#L1-L74)

**Section sources**
- [layouts/DashboardLayout.vue:1-125](file://frontend/src/layouts/DashboardLayout.vue#L1-L125)
- [components/layout/Sidebar.vue:1-258](file://frontend/src/components/layout/Sidebar.vue#L1-L258)
- [components/layout/SidebarItem.vue:1-74](file://frontend/src/components/layout/SidebarItem.vue#L1-L74)

### Reusable UI Components
Button component demonstrates:
- Variants and sizes via class variance authority
- Support for tag switching (button/a/span/etc.)
- Composable class merging with cn

ThemeToggle integrates:
- Dropdown menu for theme selection
- Delegates to theme store to apply CSS classes

```mermaid
classDiagram
class Button {
+variant : string
+size : string
+as : string
+disabled : boolean
+classes
}
class ThemeToggle {
+toggle theme options
}
ThemeToggle --> ThemeStore : "uses"
```

**Diagram sources**
- [components/ui/Button.vue:1-66](file://frontend/src/components/ui/Button.vue#L1-L66)
- [components/ui/ThemeToggle.vue:1-36](file://frontend/src/components/ui/ThemeToggle.vue#L1-L36)
- [stores/theme.js:1-53](file://frontend/src/stores/theme.js#L1-L53)

**Section sources**
- [components/ui/Button.vue:1-66](file://frontend/src/components/ui/Button.vue#L1-L66)
- [components/ui/ThemeToggle.vue:1-36](file://frontend/src/components/ui/ThemeToggle.vue#L1-L36)
- [stores/theme.js:1-53](file://frontend/src/stores/theme.js#L1-L53)

### Plugin View Integration and Data Flow
Incidents plugin view illustrates:
- Fetching data via authStore.authFetch
- Creating/updating resources with proper HTTP methods
- Rendering lists with severity/status badges and action buttons
- Using dynamic components for icons

```mermaid
sequenceDiagram
participant V as "IncidentsList.vue"
participant AS as "Auth Store"
participant BE as "Backend API"
V->>AS : "authFetch('/api/v1/plugins/incidents/')"
AS->>BE : "GET /api/v1/plugins/incidents/"
BE-->>AS : "200 [incidents]"
AS-->>V : "incidents"
V->>AS : "authFetch('/api/v1/plugins/incidents/', POST)"
AS->>BE : "POST /api/v1/plugins/incidents/"
BE-->>AS : "200 Created"
AS-->>V : "success"
V->>AS : "authFetch('/api/v1/plugins/incidents/ : id', PUT)"
AS->>BE : "PUT /api/v1/plugins/incidents/ : id"
BE-->>AS : "200 OK"
AS-->>V : "updated"
```

**Diagram sources**
- [plugins/incidents/views/IncidentsList.vue:41-104](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L104)
- [stores/auth.js:160-177](file://frontend/src/stores/auth.js#L160-L177)

**Section sources**
- [plugins/incidents/views/IncidentsList.vue:1-268](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L1-L268)
- [stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)

### Theme Management
Theme store:
- Tracks selected theme and system preference
- Applies CSS class to document element for dark mode
- Watches theme changes and updates DOM accordingly
- Initializes listener for OS theme changes

```mermaid
flowchart TD
Init(["initTheme()"]) --> WatchOS["Listen to OS theme changes"]
WatchOS --> UpdateSys["Update systemTheme"]
Select["setTheme(newTheme)"] --> Persist["Persist to localStorage"]
Persist --> Apply["Apply CSS class to root"]
Apply --> Render["Components re-render with new theme"]
```

**Diagram sources**
- [stores/theme.js:32-42](file://frontend/src/stores/theme.js#L32-L42)

**Section sources**
- [stores/theme.js:1-53](file://frontend/src/stores/theme.js#L1-L53)
- [assets/css/main.css:31-51](file://frontend/src/assets/css/main.css#L31-L51)

## Dependency Analysis
External dependencies and integrations:
- Vue 3, Vue Router, Pinia for framework and state
- lucide-vue-next for icons
- class-variance-authority, clsx, tailwind-merge for component styling
- Tailwind CSS for utility-first styling and dark mode
- Vite for dev/build tooling with proxy to backend

```mermaid
graph LR
Pkg["package.json"] --> Vue["vue"]
Pkg --> Router["vue-router"]
Pkg --> Pinia["pinia"]
Pkg --> Icons["lucide-vue-next"]
Pkg --> CVA["class-variance-authority"]
Pkg --> CLX["clsx"]
Pkg --> TWM["tailwind-merge"]
Pkg --> TW["tailwindcss"]
Pkg --> Vite["vite"]
Vite --> Alias["@ alias"]
Vite --> Proxy["/api proxy -> 8000"]
```

**Diagram sources**
- [package.json:11-29](file://frontend/package.json#L11-L29)
- [vite.config.cjs:5-22](file://frontend/vite.config.cjs#L5-L22)

**Section sources**
- [package.json:1-30](file://frontend/package.json#L1-L30)
- [vite.config.cjs:1-23](file://frontend/vite.config.cjs#L1-L23)
- [tailwind.config.js:1-59](file://frontend/tailwind.config.js#L1-L59)

## Performance Considerations
- Lazy loading of plugin routes reduces initial bundle size
- Component composition and shared UI primitives minimize duplication
- Tailwind CSS utility classes reduce CSS overhead while enabling rapid iteration
- Local storage caching for tokens avoids repeated network requests during sessions
- Dark mode via CSS classes avoids expensive runtime computations
- Vite’s development server with proxy enables efficient local iteration

Recommendations:
- Keep plugin manifests minimal; defer heavy assets to plugin views
- Use Suspense boundaries for long-loading plugin routes if needed
- Debounce frequent UI interactions (filters, search) in plugin views
- Consider pagination for large datasets in plugin views
- Audit Tailwind classes to remove unused styles in production builds

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- Authentication failures:
  - Verify tokens in localStorage and expiry timestamps
  - Ensure authFetch handles 401 and refresh flow
  - Confirm backend endpoints are reachable via proxy
- Plugin menu missing:
  - Check backend plugin list endpoint and status field
  - Confirm plugin registry initialization flag
- Theme not applying:
  - Ensure CSS class is applied to document root
  - Verify Tailwind dark mode configuration
- Styling inconsistencies:
  - Confirm Tailwind directives and custom properties are present
  - Check for conflicting CSS overrides

**Section sources**
- [stores/auth.js:136-177](file://frontend/src/stores/auth.js#L136-L177)
- [main.js:18-51](file://frontend/src/main.js#L18-L51)
- [stores/theme.js:23-42](file://frontend/src/stores/theme.js#L23-L42)
- [assets/css/main.css:1-77](file://frontend/src/assets/css/main.css#L1-L77)

## Conclusion
The frontend employs a clean, modular architecture centered on Vue 3, Pinia, and Vue Router. The plugin registry system enables dynamic integration of features, while the layout and UI components provide a consistent, accessible, and responsive experience. Theme management and Tailwind CSS support both light and dark modes. The authentication store ensures secure, resilient communication with backend APIs. Together, these patterns deliver a scalable and maintainable frontend foundation.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Responsive Design Principles
- Mobile-first layout with breakpoint-aware spacing and typography
- Collapsible sidebar for small screens with overlay and slide transitions
- Grid-based plugin views adapt to screen size
- Accessible focus states and semantic markup

**Section sources**
- [layouts/DashboardLayout.vue:23-124](file://frontend/src/layouts/DashboardLayout.vue#L23-L124)
- [plugins/incidents/views/IncidentsList.vue:198-265](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L198-L265)
- [assets/css/main.css:54-77](file://frontend/src/assets/css/main.css#L54-L77)

### Accessibility Considerations
- Semantic HTML and proper labeling for inputs and buttons
- Keyboard navigable dropdown menus and collapsible sections
- Focus-visible outlines and visible focus states
- Color contrast compliant with Tailwind color tokens
- ARIA-friendly component composition

**Section sources**
- [components/ui/Button.vue:25-53](file://frontend/src/components/ui/Button.vue#L25-L53)
- [components/layout/SidebarItem.vue:34-72](file://frontend/src/components/layout/SidebarItem.vue#L34-L72)