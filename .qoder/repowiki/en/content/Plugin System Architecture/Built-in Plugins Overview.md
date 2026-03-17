# Built-in Plugins Overview

<cite>
**Referenced Files in This Document**
- [plugin_loader.py](file://backend/app/core/plugin_loader.py)
- [config.py](file://backend/app/core/config.py)
- [main.py](file://backend/app/main.py)
- [plugin.py (Incidents)](file://backend/app/plugins/incidents/plugin.py)
- [endpoints.py (Incidents)](file://backend/app/plugins/incidents/endpoints.py)
- [plugin.py (Inventory)](file://backend/app/plugins/inventory/plugin.py)
- [endpoints.py (Inventory)](file://backend/app/plugins/inventory/endpoints.py)
- [plugin.py (Performance)](file://backend/app/plugins/performance/plugin.py)
- [endpoints.py (Performance)](file://backend/app/plugins/performance/endpoints.py)
- [plugin.py (Security Module)](file://backend/app/plugins/security_module/plugin.py)
- [plugin.py (Accounting)](file://backend/app/plugins/accounting/plugin.py)
- [plugin.py (Configuration)](file://backend/app/plugins/configuration/plugin.py)
- [plugin.py (IPAM)](file://backend/app/plugins/ipam/plugin.py)
- [endpoints.py (IPAM)](file://backend/app/plugins/ipam/endpoints.py)
- [plugin.py (Customer Services)](file://backend/app/plugins/customer_services/plugin.py)
- [endpoints.py (Customer Services)](file://backend/app/plugins/customer_services/endpoints.py)
- [models.py (Customer Services)](file://backend/app/plugins/customer_services/models.py)
- [schemas.py (Customer Services)](file://backend/app/plugins/customer_services/schemas.py)
- [pluginRegistry.js](file://frontend/src/stores/pluginRegistry.js)
- [IncidentsList.vue](file://frontend/src/plugins/incidents/views/IncidentsList.vue)
- [Performance.vue](file://frontend/src/plugins/performance/views/Performance.vue)
- [Ipam.vue](file://frontend/src/plugins/ipam/views/Ipam.vue)
- [CustomerServices.vue](file://frontend/src/plugins/customer_services/views/CustomerServices.vue)
</cite>

## Update Summary
**Changes Made**
- Added comprehensive documentation for the Customer Services plugin as the 8th built-in plugin
- Updated the plugin count from 7 to 8 built-in plugins
- Enhanced the architecture overview to include Customer Services plugin examples
- Updated configuration and selection criteria to include Customer Services plugin
- Added detailed component analysis for Customer Services plugin functionality including CSV import, real-time updates, and statistics dashboard
- Updated frontend integration documentation to include Customer Services Vue component

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
This document provides a comprehensive overview of the eight built-in plugins that ship with the system: Incidents, Inventory, Performance, Security Module, Accounting, Configuration, IPAM, and Customer Services. It explains each plugin's purpose, functionality, and integration within the overall platform, and demonstrates how these plugins illustrate the plugin architecture and serve as examples for developing custom plugins. It also covers plugin selection criteria, enable/disable mechanisms, and configuration options for each built-in plugin.

## Project Structure
The plugin system is implemented in the backend under a dedicated plugins directory. Each plugin exposes a plugin registration module and an API router. The backend loads plugins at startup, constructs per-plugin API prefixes, and registers routers with the main application. The frontend integrates plugin-managed UI views and menus via a plugin registry store.

```mermaid
graph TB
subgraph "Backend"
MAIN["main.py<br/>FastAPI app"]
LOADER["plugin_loader.py<br/>load_plugins()"]
CFG["config.py<br/>Settings"]
PLUG_INC["plugins/incidents/plugin.py"]
PLUG_INV["plugins/inventory/plugin.py"]
PLUG_PERF["plugins/performance/plugin.py"]
PLUG_SEC["plugins/security_module/plugin.py"]
PLUG_ACC["plugins/accounting/plugin.py"]
PLUG_CFG["plugins/configuration/plugin.py"]
PLUG_IPAM["plugins/ipam/plugin.py"]
PLUG_CS["plugins/customer_services/plugin.py"]
API_INC["plugins/incidents/endpoints.py"]
API_INV["plugins/inventory/endpoints.py"]
API_PERF["plugins/performance/endpoints.py"]
API_IPAM["plugins/ipam/endpoints.py"]
API_CS["plugins/customer_services/endpoints.py"]
end
subgraph "Frontend"
REG["pluginRegistry.js<br/>Pinia store"]
VIEW_INC["IncidentsList.vue"]
VIEW_PERF["Performance.vue"]
VIEW_IPAM["Ipam.vue"]
VIEW_CS["CustomerServices.vue"]
end
MAIN --> LOADER
LOADER --> CFG
LOADER --> PLUG_INC
LOADER --> PLUG_INV
LOADER --> PLUG_PERF
LOADER --> PLUG_SEC
LOADER --> PLUG_ACC
LOADER --> PLUG_CFG
LOADER --> PLUG_IPAM
LOADER --> PLUG_CS
PLUG_INC --> API_INC
PLUG_INV --> API_INV
PLUG_PERF --> API_PERF
PLUG_IPAM --> API_IPAM
PLUG_CS --> API_CS
MAIN --> API_INC
MAIN --> API_INV
MAIN --> API_PERF
MAIN --> API_IPAM
MAIN --> API_CS
REG --> VIEW_INC
REG --> VIEW_PERF
REG --> VIEW_IPAM
REG --> VIEW_CS
```

**Diagram sources**
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [plugin.py (Incidents):9-17](file://backend/app/plugins/incidents/plugin.py#L9-L17)
- [plugin.py (Inventory):9-17](file://backend/app/plugins/inventory/plugin.py#L9-L17)
- [plugin.py (Performance):9-17](file://backend/app/plugins/performance/plugin.py#L9-L17)
- [plugin.py (Security Module):9-17](file://backend/app/plugins/security_module/plugin.py#L9-L17)
- [plugin.py (Accounting):9-17](file://backend/app/plugins/accounting/plugin.py#L9-L17)
- [plugin.py (Configuration):9-17](file://backend/app/plugins/configuration/plugin.py#L9-L17)
- [plugin.py (IPAM):9-17](file://backend/app/plugins/ipam/plugin.py#L9-L17)
- [plugin.py (Customer Services):9-17](file://backend/app/plugins/customer_services/plugin.py#L9-L17)
- [endpoints.py (Incidents):15](file://backend/app/plugins/incidents/endpoints.py#L15)
- [endpoints.py (Inventory):15](file://backend/app/plugins/inventory/endpoints.py#L15)
- [endpoints.py (Performance):11](file://backend/app/plugins/performance/endpoints.py#L11)
- [endpoints.py (IPAM):20-109](file://backend/app/plugins/ipam/endpoints.py#L20-L109)
- [endpoints.py (Customer Services):18-172](file://backend/app/plugins/customer_services/endpoints.py#L18-172)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)
- [IncidentsList.vue:1-268](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L1-L268)
- [Performance.vue:1-34](file://frontend/src/plugins/performance/views/Performance.vue#L1-L34)
- [Ipam.vue:1-489](file://frontend/src/plugins/ipam/views/Ipam.vue#L1-L489)
- [CustomerServices.vue:1-384](file://frontend/src/plugins/customer_services/views/CustomerServices.vue#L1-L384)

**Section sources**
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)

## Core Components
- Plugin loader: Discovers plugin directories, conditionally enables plugins, imports models and plugin modules, constructs a per-plugin API prefix, and registers routers into the main application.
- Plugin registration: Each plugin defines metadata and a register function that includes the plugin's router with a tag and a plugin-scoped API prefix.
- Configuration: The settings object exposes an environment variable to filter enabled plugins.
- Frontend plugin registry: A Pinia store manages plugin manifests, enabled plugins, and aggregated menu items for rendering.

Key behaviors:
- Discovery: Iterates over the plugins directory, skipping hidden or invalid entries.
- Filtering: Uses a comma-separated list from settings to include only named plugins.
- Registration: Builds a PluginContext with database base, API prefix, and dependency injection helpers, then invokes register.
- API prefixing: Each plugin receives a distinct API prefix derived from its plugin name.

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [plugin.py (Incidents):1-17](file://backend/app/plugins/incidents/plugin.py#L1-L17)
- [plugin.py (Inventory):1-17](file://backend/app/plugins/inventory/plugin.py#L1-L17)
- [plugin.py (Performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [plugin.py (Security Module):1-17](file://backend/app/plugins/security_module/plugin.py#L1-L17)
- [plugin.py (Accounting):1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)
- [plugin.py (Configuration):1-17](file://backend/app/plugins/configuration/plugin.py#L1-L17)
- [plugin.py (IPAM):1-17](file://backend/app/plugins/ipam/plugin.py#L1-L17)
- [plugin.py (Customer Services):1-17](file://backend/app/plugins/customer_services/plugin.py#L1-L17)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

## Architecture Overview
The plugin architecture centers on a shared loader and per-plugin modules. At startup, the loader:
- Reads settings to determine enabled plugins.
- Imports each plugin's models (if present) and plugin module.
- Extracts metadata and register function.
- Constructs a PluginContext and calls register to attach the plugin's router to the main app.

```mermaid
sequenceDiagram
participant App as "FastAPI App"
participant Loader as "load_plugins()"
participant Settings as "Settings"
participant Mod as "Plugin Module"
participant Router as "Plugin Router"
App->>Loader : "Startup lifecycle"
Loader->>Settings : "Read ENABLED_PLUGINS"
loop "For each plugin dir"
Loader->>Mod : "Import models (optional)"
Loader->>Mod : "Import plugin.py"
Loader->>Mod : "Get PLUGIN_META/register"
Loader->>App : "Build PluginContext and call register"
App->>Router : "include_router(prefix, tags)"
end
App-->>App : "Expose /api/v1/plugins for status"
```

**Diagram sources**
- [main.py:17-48](file://backend/app/main.py#L17-L48)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [plugin.py (Incidents):9-17](file://backend/app/plugins/incidents/plugin.py#L9-L17)
- [plugin.py (Inventory):9-17](file://backend/app/plugins/inventory/plugin.py#L9-L17)
- [plugin.py (Performance):9-17](file://backend/app/plugins/performance/plugin.py#L9-L17)
- [plugin.py (Security Module):9-17](file://backend/app/plugins/security_module/plugin.py#L9-L17)
- [plugin.py (Accounting):9-17](file://backend/app/plugins/accounting/plugin.py#L9-L17)
- [plugin.py (Configuration):9-17](file://backend/app/plugins/configuration/plugin.py#L9-L17)
- [plugin.py (IPAM):9-17](file://backend/app/plugins/ipam/plugin.py#L9-L17)
- [plugin.py (Customer Services):9-17](file://backend/app/plugins/customer_services/plugin.py#L9-L17)

## Detailed Component Analysis

### Incidents Plugin
Purpose:
- Incident management for creating, tracking, and resolving network incidents.

Functionality:
- Provides endpoints to list, create, retrieve, update, and delete incidents.
- Supports incident comments and enforces role-based access for administrative actions.
- Frontend view displays incidents with severity and status badges and supports status transitions.

Integration:
- Register function attaches the incidents router with a plugin-specific API prefix and tags.
- Frontend fetches data from the incidents API and renders a responsive card-based list.

```mermaid
sequenceDiagram
participant FE as "IncidentsList.vue"
participant Auth as "Auth Store"
participant API as "Incidents API"
participant DB as "SQLAlchemy ORM"
FE->>Auth : "authFetch('/api/v1/plugins/incidents/')"
Auth->>API : "GET /"
API->>DB : "Query incidents ordered by created_at desc"
DB-->>API : "List[Incident]"
API-->>FE : "JSON incidents"
FE->>FE : "Render cards and controls"
```

**Diagram sources**
- [IncidentsList.vue:41-55](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L41-L55)
- [endpoints.py (Incidents):18-25](file://backend/app/plugins/incidents/endpoints.py#L18-L25)
- [plugin.py (Incidents):9-17](file://backend/app/plugins/incidents/plugin.py#L9-L17)

Configuration and selection:
- Enable/disable via settings using the plugin directory name "incidents".
- API exposed under /api/v1/plugins/incidents.

**Section sources**
- [plugin.py (Incidents):1-17](file://backend/app/plugins/incidents/plugin.py#L1-L17)
- [endpoints.py (Incidents):18-84](file://backend/app/plugins/incidents/endpoints.py#L18-L84)
- [IncidentsList.vue:1-268](file://frontend/src/plugins/incidents/views/IncidentsList.vue#L1-L268)

### Inventory Plugin
Purpose:
- Equipment inventory management covering devices, sites, and device types.

Functionality:
- CRUD endpoints for devices, sites, and device types with role-based permissions.
- Supports listing, creating, retrieving, updating, and deleting resources.

Integration:
- Register function attaches the inventory router with a plugin-specific API prefix and tags.

```mermaid
sequenceDiagram
participant FE as "Inventory UI"
participant API as "Inventory API"
participant DB as "SQLAlchemy ORM"
FE->>API : "GET /api/v1/plugins/inventory/devices"
API->>DB : "Query Device"
DB-->>API : "List[Device]"
API-->>FE : "JSON devices"
```

**Diagram sources**
- [endpoints.py (Inventory):20-83](file://backend/app/plugins/inventory/endpoints.py#L20-L83)
- [plugin.py (Inventory):9-17](file://backend/app/plugins/inventory/plugin.py#L9-L17)

Configuration and selection:
- Enable/disable via settings using the plugin directory name "inventory".

**Section sources**
- [plugin.py (Inventory):1-17](file://backend/app/plugins/inventory/plugin.py#L1-L17)
- [endpoints.py (Inventory):18-130](file://backend/app/plugins/inventory/endpoints.py#L18-L130)

### Performance Plugin
Purpose:
- Network performance monitoring with monitor targets and metric samples.

Functionality:
- CRUD endpoints for monitor targets and retrieval of metric samples for a given target.
- Supports listing, creating, retrieving, and deleting monitor targets; fetching recent metrics.

Integration:
- Register function attaches the performance router with a plugin-specific API prefix and tags.

```mermaid
sequenceDiagram
participant FE as "Performance.vue"
participant API as "Performance API"
participant DB as "SQLAlchemy ORM"
FE->>API : "GET /api/v1/plugins/performance/targets"
API->>DB : "Query MonitorTarget"
DB-->>API : "List[MonitorTarget]"
API-->>FE : "JSON targets"
```

**Diagram sources**
- [endpoints.py (Performance):14-58](file://backend/app/plugins/performance/endpoints.py#L14-L58)
- [plugin.py (Performance):9-17](file://backend/app/plugins/performance/plugin.py#L9-L17)
- [Performance.vue:1-34](file://frontend/src/plugins/performance/views/Performance.vue#L1-L34)

Configuration and selection:
- Enable/disable via settings using the plugin directory name "performance".

**Section sources**
- [plugin.py (Performance):1-17](file://backend/app/plugins/performance/plugin.py#L1-L17)
- [endpoints.py (Performance):11-75](file://backend/app/plugins/performance/endpoints.py#L11-L75)

### Security Module Plugin
Purpose:
- Security module for audit logs, security events, and access monitoring.

Functionality:
- Exposes a plugin registration with a dedicated router and API prefix.
- Frontend view indicates future feature availability.

Integration:
- Register function attaches the security router with a plugin-specific API prefix and tags.

```mermaid
flowchart TD
Start(["Security Module Loaded"]) --> Router["Attach Security Router"]
Router --> Prefix["Use /api/v1/plugins/security"]
Prefix --> Tags["Tag: Security"]
Tags --> Ready["Ready for endpoints"]
```

**Diagram sources**
- [plugin.py (Security Module):9-17](file://backend/app/plugins/security_module/plugin.py#L9-L17)

Configuration and selection:
- Enable/disable via settings using the plugin directory name "security".

**Section sources**
- [plugin.py (Security Module):1-17](file://backend/app/plugins/security_module/plugin.py#L1-L17)

### Accounting Plugin
Purpose:
- Traffic accounting for interfaces, traffic records, and bandwidth usage.

Functionality:
- Exposes a plugin registration with a dedicated router and API prefix.

Integration:
- Register function attaches the accounting router with a plugin-specific API prefix and tags.

Configuration and selection:
- Enable/disable via settings using the plugin directory name "accounting".

**Section sources**
- [plugin.py (Accounting):1-17](file://backend/app/plugins/accounting/plugin.py#L1-L17)

### Configuration Plugin
Purpose:
- Configuration management including snapshots, templates, and change tracking.

Functionality:
- Exposes a plugin registration with a dedicated router and API prefix.

Integration:
- Register function attaches the configuration router with a plugin-specific API prefix and tags.

Configuration and selection:
- Enable/disable via settings using the plugin directory name "configuration".

**Section sources**
- [plugin.py (Configuration):1-17](file://backend/app/plugins/configuration/plugin.py#L1-L17)

### IPAM Plugin
**Updated** Added comprehensive documentation for the IPAM plugin

Purpose:
- NetBox IP Address Management integration for validating and managing IP addresses across network infrastructure.

Functionality:
- Provides three main API endpoints: validation, apply, and database querying.
- Supports IP address validation comparing NetBox data with actual network state.
- Enables batch application of IP address changes to NetBox.
- Offers comprehensive database querying with filtering, sorting, and pagination capabilities.

Integration:
- Register function attaches the IPAM router with a plugin-specific API prefix and "IPAM" tag.
- Frontend Vue component provides dual-tab interface for validation and database management.
- Implements sophisticated filtering, sorting, and pagination for large IP address datasets.

```mermaid
sequenceDiagram
participant FE as "Ipam.vue"
participant Auth as "Auth Store"
participant API as "IPAM API"
participant NetBox as "NetBox API"
FE->>Auth : "authFetch('/api/v1/plugins/ipam/validate')"
Auth->>API : "POST /validate"
API->>NetBox : "Execute validation script"
NetBox-->>API : "Validation results"
API-->>FE : "Added/Removed changes"
FE->>Auth : "authFetch('/api/v1/plugins/ipam/apply')"
Auth->>API : "POST /apply with changes"
API->>NetBox : "Apply changes to NetBox"
NetBox-->>API : "Confirmation"
API-->>FE : "Success response"
```

**Diagram sources**
- [Ipam.vue:53-100](file://frontend/src/plugins/ipam/views/Ipam.vue#L53-L100)
- [endpoints.py (IPAM):20-58](file://backend/app/plugins/ipam/endpoints.py#L20-L58)
- [plugin.py (IPAM):9-17](file://backend/app/plugins/ipam/plugin.py#L9-L17)

Configuration and selection:
- Enable/disable via settings using the plugin directory name "ipam".
- API exposed under /api/v1/plugins/ipam with three endpoints:
  - POST /validate - Validates IP address configuration against NetBox
  - POST /apply - Applies validated changes to NetBox
  - GET /database - Retrieves IP address database with filtering and pagination

**Section sources**
- [plugin.py (IPAM):1-17](file://backend/app/plugins/ipam/plugin.py#L1-L17)
- [endpoints.py (IPAM):20-109](file://backend/app/plugins/ipam/endpoints.py#L20-L109)
- [Ipam.vue:1-489](file://frontend/src/plugins/ipam/views/Ipam.vue#L1-L489)

### Customer Services Plugin
**New** Added comprehensive documentation for the Customer Services plugin as the 8th built-in plugin

Purpose:
- Customer services management for viewing and editing service database with CSV import capabilities.

Functionality:
- Provides comprehensive CRUD operations for customer services with advanced filtering and pagination.
- Supports CSV import functionality to populate the service database automatically.
- Includes real-time statistics dashboard showing service distribution by status.
- Features modal-based editing interface with extensive field support for service management.

Integration:
- Register function attaches the customer services router with a plugin-specific API prefix and "Customer Services" tag.
- Frontend Vue component provides table-based interface with search, filtering, pagination, and modal editing.
- Implements sophisticated data loading with automatic CSV-to-database migration.

```mermaid
sequenceDiagram
participant FE as "CustomerServices.vue"
participant Auth as "Auth Store"
participant API as "Customer Services API"
participant DB as "SQLAlchemy ORM"
FE->>Auth : "authFetch('/api/v1/plugins/customer_services/services?page=1&page_size=50')"
Auth->>API : "GET /services"
API->>DB : "Query CustomerService with filters"
DB-->>API : "Paginated results with count"
API-->>FE : "JSON with count and results"
FE->>FE : "Render table with pagination controls"
FE->>Auth : "authFetch('/api/v1/plugins/customer_services/stats')"
Auth->>API : "GET /stats"
API->>DB : "Count services and group by status"
DB-->>API : "Statistics data"
API-->>FE : "Total and status distribution"
```

**Diagram sources**
- [CustomerServices.vue:77-100](file://frontend/src/plugins/customer_services/views/CustomerServices.vue#L77-L100)
- [endpoints.py (Customer Services):69-112](file://backend/app/plugins/customer_services/endpoints.py#L69-112)
- [plugin.py (Customer Services):9-17](file://backend/app/plugins/customer_services/plugin.py#L9-L17)

Configuration and selection:
- Enable/disable via settings using the plugin directory name "customer_services".
- API exposed under /api/v1/plugins/customer_services with four endpoints:
  - GET /services - Lists services with pagination, search, and filtering
  - GET /services/{id} - Retrieves individual service by ID
  - PUT /services/{id} - Updates service information
  - GET /stats - Returns service statistics and status distribution

Data Model and Schema:
- CustomerService model includes 20+ fields covering service identification, client information, network details, and operational data.
- Automatic CSV import from CSV_PATH with semicolon-delimited format.
- Real-time statistics aggregation with status distribution counting.

Frontend Features:
- Responsive table interface with 8 visible columns and 25+ editable fields in modal view.
- Advanced filtering by search term, status, and client with live updates.
- Pagination with configurable page size (1-100 items).
- Status-based visual indicators with color coding.
- Modal-based editing with cancel/save functionality.

**Section sources**
- [plugin.py (Customer Services):1-17](file://backend/app/plugins/customer_services/plugin.py#L1-L17)
- [endpoints.py (Customer Services):18-172](file://backend/app/plugins/customer_services/endpoints.py#L18-172)
- [models.py (Customer Services):6-74](file://backend/app/plugins/customer_services/models.py#L6-74)
- [schemas.py (Customer Services):6-54](file://backend/app/plugins/customer_services/schemas.py#L6-54)
- [CustomerServices.vue:1-384](file://frontend/src/plugins/customer_services/views/CustomerServices.vue#L1-L384)

## Dependency Analysis
The plugin system exhibits low coupling and high cohesion:
- Backend loader depends on settings and dynamically imports plugin modules.
- Each plugin module depends only on the loader's PluginContext and FastAPI router.
- Frontend registry depends on plugin manifests and aggregates menu items.

```mermaid
graph LR
Settings["Settings.ENABLED_PLUGINS"] --> Loader["load_plugins()"]
Loader --> PluginMeta["PLUGIN_META"]
Loader --> RegisterFn["register(app, context)"]
RegisterFn --> Router["APIRouter"]
Router --> MainApp["FastAPI app.include_router(...)"]
FEStore["pluginRegistry.js"] --> Manifests["Plugin manifests"]
Manifests --> Menu["Aggregated menu items"]
```

**Diagram sources**
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [plugin.py (Incidents):1-17](file://backend/app/plugins/incidents/plugin.py#L1-L17)
- [plugin.py (IPAM):1-17](file://backend/app/plugins/ipam/plugin.py#L1-L17)
- [plugin.py (Customer Services):1-17](file://backend/app/plugins/customer_services/plugin.py#L1-L17)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [pluginRegistry.js:1-53](file://frontend/src/stores/pluginRegistry.js#L1-L53)

## Performance Considerations
- Plugin discovery iterates over the plugins directory; keep the number of plugins reasonable for large deployments.
- Per-plugin API prefixing avoids naming conflicts but increases routing surface; ensure efficient router organization.
- Role-based endpoints (admin vs active user) reduce unnecessary processing for non-admin operations.
- Consider pagination and filtering in endpoints to minimize payload sizes for large datasets.
- **Updated** IPAM plugin endpoints support pagination and filtering for large IP address datasets, with configurable page sizes up to 100 items.
- **Updated** Customer Services plugin implements efficient CSV import with existence checks to prevent duplicate data loading.
- **Updated** Customer Services plugin uses SQLAlchemy's count() method for efficient pagination without loading all records.

## Troubleshooting Guide
Common issues and resolutions:
- Plugin not loaded:
  - Verify the plugin directory contains a plugin.py with PLUGIN_META and register.
  - Confirm the plugin name is included in the ENABLED_PLUGINS setting.
- API route not visible:
  - Ensure the register function includes the router with the correct prefix and tags.
  - Check that models are imported before registering routers to ensure database tables are created.
- Frontend menu missing:
  - Ensure the plugin manifest is registered in the frontend plugin registry store.
  - Confirm the manifest's enabled flag and menu items are properly set.
- **Updated** IPAM plugin specific issues:
  - Validation endpoint returns empty results: Verify NetBox connectivity and authentication.
  - Apply endpoint fails: Check NetBox API credentials and permissions.
  - Database endpoint slow: Use pagination parameters and filters to reduce payload size.
- **Updated** Customer Services plugin specific issues:
  - CSV import not working: Verify CSV file exists at CSV_PATH and has correct semicolon delimiter format.
  - Services endpoint returns empty: Check database connection and ensure CSV data was successfully imported.
  - Modal editing fails: Verify user authentication and proper field validation.
  - Statistics endpoint slow: Large datasets may require pagination or filtering optimization.

Operational checks:
- Startup logs indicate plugin load status and any errors encountered during import.
- The /api/v1/plugins endpoint returns the list of loaded plugins with status.

**Section sources**
- [plugin_loader.py:25-99](file://backend/app/core/plugin_loader.py#L25-L99)
- [main.py:84-87](file://backend/app/main.py#L84-L87)
- [pluginRegistry.js:26-36](file://frontend/src/stores/pluginRegistry.js#L26-L36)

## Conclusion
The eight built-in plugins showcase a clean, extensible plugin architecture. They demonstrate consistent patterns for metadata definition, registration, API prefixing, and role-aware endpoints. Their integration with the loader and frontend registry provides a practical blueprint for building custom plugins. Administrators can selectively enable or disable plugins via configuration, while developers can extend the system by adding new plugin directories following the established conventions. The IPAM plugin exemplifies the complete plugin lifecycle with sophisticated API endpoints and comprehensive frontend integration. The newly added Customer Services plugin demonstrates advanced features including CSV import, real-time statistics, and comprehensive data management capabilities.

## Appendices

### Plugin Selection Criteria and Enable/Disable Mechanism
- Selection criteria:
  - Presence of a plugin.py with PLUGIN_META and register.
  - Directory name matches an entry in ENABLED_PLUGINS (comma-separated).
- Enable/disable:
  - Set ENABLED_PLUGINS to a comma-separated list of plugin directory names.
  - Omitting the setting loads all discovered plugins.

**Section sources**
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [plugin_loader.py:33-48](file://backend/app/core/plugin_loader.py#L33-L48)

### Configuration Options for Built-in Plugins
- Global:
  - ENABLED_PLUGINS: Comma-separated list of plugin names to load.
- Plugin-specific:
  - Each plugin's API prefix is automatically constructed as /api/v1/plugins/{plugin_name}.
  - Tags are applied per plugin for API documentation grouping.
- **Updated** IPAM Plugin Endpoints:
  - POST /validate: Validates IP address configuration against NetBox
  - POST /apply: Applies validated changes to NetBox
  - GET /database: Retrieves IP address database with filtering and pagination
- **Updated** Customer Services Plugin Endpoints:
  - GET /services: Lists services with pagination, search, and filtering
  - GET /services/{id}: Retrieves individual service by ID
  - PUT /services/{id}: Updates service information
  - GET /stats: Returns service statistics and status distribution

**Section sources**
- [config.py:25-26](file://backend/app/core/config.py#L25-L26)
- [plugin_loader.py:70-76](file://backend/app/core/plugin_loader.py#L70-L76)
- [plugin.py (Incidents):12-16](file://backend/app/plugins/incidents/plugin.py#L12-L16)
- [plugin.py (Inventory):12-16](file://backend/app/plugins/inventory/plugin.py#L12-L16)
- [plugin.py (Performance):12-16](file://backend/app/plugins/performance/plugin.py#L12-L16)
- [plugin.py (Security Module):12-16](file://backend/app/plugins/security_module/plugin.py#L12-L16)
- [plugin.py (Accounting):12-16](file://backend/app/plugins/accounting/plugin.py#L12-L16)
- [plugin.py (Configuration):12-16](file://backend/app/plugins/configuration/plugin.py#L12-L16)
- [plugin.py (IPAM):12-16](file://backend/app/plugins/ipam/plugin.py#L12-L16)
- [plugin.py (Customer Services):12-16](file://backend/app/plugins/customer_services/plugin.py#L12-L16)
- [endpoints.py (IPAM):20-109](file://backend/app/plugins/ipam/endpoints.py#L20-L109)
- [endpoints.py (Customer Services):18-172](file://backend/app/plugins/customer_services/endpoints.py#L18-172)