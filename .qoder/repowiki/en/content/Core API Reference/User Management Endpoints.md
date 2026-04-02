# User Management Endpoints

<cite>
**Referenced Files in This Document**
- [users.py](file://backend/app/api/v1/endpoints/users.py)
- [router.py](file://backend/app/api/v1/router.py)
- [user.py](file://backend/app/models/user.py)
- [user.py](file://backend/app/schemas/user.py)
- [common.py](file://backend/app/schemas/common.py)
- [security.py](file://backend/app/core/security.py)
- [main.py](file://backend/app/main.py)
- [auth.py](file://backend/app/api/v1/endpoints/auth.py)
- [user_service.py](file://backend/app/services/user_service.py)
- [002_add_background_image_to_users.py](file://backend/alembic/versions/002_add_background_image_to_users.py)
- [Avatar.vue](file://frontend/src/components/ui/Avatar.vue)
- [Profile.vue](file://frontend/src/views/settings/Profile.vue)
- [Display.vue](file://frontend/src/views/settings/Display.vue)
- [theme.js](file://frontend/src/stores/theme.js)
- [auth.js](file://frontend/src/stores/auth.js)
</cite>

## Update Summary
**Changes Made**
- Added new unified PUT /api/v1/users/me endpoint for comprehensive user profile updates
- Enhanced UserUpdate schema with theme field for color theme preferences
- Added theme field to User model with database support
- Updated UserResponse schema with theme field for complete profile representation
- Enhanced existing user management capabilities with unified update functionality
- Integrated theme preferences with frontend theme store and display settings

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
This document provides comprehensive API documentation for user management endpoints within the NOC Vision platform. It covers HTTP methods, URL patterns, request/response schemas, authorization requirements, role-based access control, and practical usage examples for user CRUD operations, bulk operations, user search/filtering, avatar management, background management, and theme preferences functionality. The documentation focuses on the `/api/v1/users/` endpoint group and related authentication endpoints that support user lifecycle management, including new unified profile update capabilities and comprehensive user customization options.

## Project Structure
The user management functionality is organized under the FastAPI application with modular routing and schema-driven validation. The key components include:
- Endpoint definitions for user operations, permission management, avatar management, background management, and unified profile updates
- Pydantic models for request/response schemas with avatar, background, and theme support
- SQLAlchemy models for persistence with avatar URL, background image, and theme storage
- Security utilities for authentication, authorization, and plugin access control
- Router configuration for API versioning
- Frontend integration for avatar selection, upload, background customization, and theme preferences
- Database migration support for background image and theme fields

```mermaid
graph TB
A["FastAPI Application<br/>main.py"] --> B["API Router v1<br/>router.py"]
B --> C["Users Router<br/>users.py"]
B --> D["Auth Router<br/>auth.py"]
C --> E["User Service<br/>user_service.py"]
D --> F["Auth Service<br/>auth_service.py"]
E --> G["User Model<br/>models/user.py"]
F --> G
C --> H["User Schemas<br/>schemas/user.py"]
D --> I["Auth Schemas<br/>schemas/auth.py"]
C --> J["Common Schemas<br/>schemas/common.py"]
K["Security Utilities<br/>core/security.py"] --> C
K --> D
L["Frontend Avatar Component<br/>Avatar.vue"] --> M["Profile View<br/>Profile.vue"]
N["Frontend Theme Store<br/>theme.js"] --> O["Display Settings<br/>Display.vue"]
P["Theme Preferences<br/>users/me"] --> C
Q["Background Image Migration<br/>002_add_background_image_to_users.py"] --> G
R["Background Management<br/>users/me/background"] --> C
S["Background List<br/>users/me/backgrounds-list"] --> C
T["Unified Profile Update<br/>users/me"] --> C
M --> O
O --> P
O --> Q
O --> R
O --> S
P --> T
```

**Diagram sources**
- [main.py:66-67](file://backend/app/main.py#L66-L67)
- [router.py:6-9](file://backend/app/api/v1/router.py#L6-L9)
- [users.py:12](file://backend/app/api/v1/endpoints/users.py#L12)
- [auth.py:17](file://backend/app/api/v1/endpoints/auth.py#L17)
- [Avatar.vue:1-58](file://frontend/src/components/ui/Avatar.vue#L1-L58)
- [Profile.vue:1-199](file://frontend/src/views/settings/Profile.vue#L1-L199)
- [Display.vue:1-202](file://frontend/src/views/settings/Display.vue#L1-L202)
- [theme.js:1-104](file://frontend/src/stores/theme.js#L1-L104)
- [auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)
- [002_add_background_image_to_users.py:21-22](file://backend/alembic/versions/002_add_background_image_to_users.py#L21-L22)

**Section sources**
- [main.py:66-67](file://backend/app/main.py#L66-L67)
- [router.py:6-9](file://backend/app/api/v1/router.py#L6-L9)

## Core Components
This section outlines the essential building blocks for user management operations:

### Authentication and Authorization
- OAuth2 Bearer token scheme with JWT tokens
- Enhanced role-based access control with superuser privileges
- Plugin access control for different sections (operations, analytics, security, admin)
- Password hashing using bcrypt
- Token validation and expiration handling

### Data Models
- User entity with unique constraints on username and email
- Role enumeration with superuser, admin, and user values
- Active/inactive user status management
- Timestamp tracking for created/updated records
- **Updated**: Avatar URL field with system avatar support (system:1, system:2, system:3)
- **Updated**: Background image field for user desktop customization
- **Updated**: Theme field for color theme preferences (light, dark, system)

### Request/Response Schemas
- User creation with username, email, password, full name, role, optional avatar URL, optional background image, and optional theme
- User updates with selective field updates including avatar URL, background image, and theme preferences
- User response with comprehensive profile information including avatar URL, background image, and theme preferences
- Status responses for deletion operations
- Permission response with role-based access information
- **Updated**: Avatar URL, background image, and theme fields in all schemas for comprehensive profile customization

**Section sources**
- [security.py:13](file://backend/app/core/security.py#L13)
- [user.py:7-18](file://backend/app/models/user.py#L7-L18)
- [user.py:6-32](file://backend/app/schemas/user.py#L6-L32)

## Architecture Overview
The user management architecture follows a layered approach with clear separation of concerns and enhanced security controls:

```mermaid
sequenceDiagram
participant Client as "Client Application"
participant API as "FastAPI Router"
participant Endpoint as "Users Endpoint"
participant Service as "User Service"
participant DB as "Database"
participant Security as "Security Layer"
Client->>API : HTTP Request
API->>Endpoint : Route to Users Endpoint
Endpoint->>Security : Validate JWT Token & Check Permissions
Security-->>Endpoint : Authorized User Context
Endpoint->>Service : Business Logic Call (including unified profile update)
Service->>DB : Database Operation
DB-->>Service : Data Result
Service-->>Endpoint : Processed Data
Endpoint-->>Client : JSON Response
```

**Diagram sources**
- [users.py:15-22](file://backend/app/api/v1/endpoints/users.py#L15-L22)
- [security.py:61-98](file://backend/app/core/security.py#L61-L98)
- [user_service.py:8-9](file://backend/app/services/user_service.py#L8-L9)

The architecture enforces:
- Centralized authentication through OAuth2 Bearer tokens
- Enhanced role-based authorization for sensitive operations
- Plugin access control for different system sections
- Schema validation at the endpoint level
- Database abstraction through SQLAlchemy ORM
- **Updated**: Unified profile update functionality with comprehensive field validation
- **Updated**: Theme preferences integration with frontend theme store

## Detailed Component Analysis

### Endpoint Definitions and URL Patterns
The user management endpoints follow RESTful conventions with the base path `/api/v1/users` and include new permission endpoints, avatar management functionality, background management endpoints, and unified profile update capabilities:

#### PUT /api/v1/users/me
- **Purpose**: Unified profile update for current user (theme, background, avatar, email, full name, password)
- **Method**: PUT
- **Request Body**: UserUpdate schema with allowed fields: theme, background_image, full_name, email, avatar_url, password
- **Response**: UserResponse object with updated profile information
- **Authorization**: Requires valid JWT token (any authenticated user)
- **Validation**: Only allowed fields are processed; password updates trigger re-hashing
- **Response Fields**:
  - `theme`: Color theme preference (light, dark, system)
  - `background_image`: Background image filename or null
  - `avatar_url`: Updated avatar URL or system avatar identifier
  - `email`: Updated email address
  - `full_name`: Updated full name
  - `password`: Hashed password (only when provided)

#### PUT /api/v1/users/me/avatar
- **Purpose**: Update the current user's avatar
- **Method**: PUT
- **Request Body**: `{ avatar_url: string }`
- **Response**: UserResponse object with updated avatar URL
- **Authorization**: Requires valid JWT token (any authenticated user)
- **Validation**: Avatar URL must be a valid URL or system avatar format (system:1, system:2, system:3)
- **Response Fields**:
  - `avatar_url`: Updated avatar URL or system avatar identifier

#### PUT /api/v1/users/me/background
- **Purpose**: Update the current user's background image preference
- **Method**: PUT
- **Request Body**: `{ background_image: string }`
- **Response**: UserResponse object with updated background image
- **Authorization**: Requires valid JWT token (any authenticated user)
- **Validation**: Background image must be a valid filename from the available backgrounds list or null to clear
- **Response Fields**:
  - `background_image`: Updated background image filename or null

#### GET /api/v1/users/me/backgrounds-list
- **Purpose**: Retrieve list of available background images
- **Method**: GET
- **Response**: Backgrounds list with available image filenames
- **Authorization**: Requires valid JWT token (any authenticated user)
- **Response Fields**:
  - `backgrounds`: Array of available background image filenames
- **Implementation Details**:
  - Searches in `/usr/share/nginx/html/backgrounds` (production nginx static directory)
  - Falls back to `frontend/public/backgrounds` (development directory)
  - Supports file extensions: jpg, jpeg, png, webp, gif, avif

#### GET /api/v1/users/me/permissions
- **Purpose**: Retrieve current user's permission information
- **Method**: GET
- **Response**: Permission object with role, superuser flag, and accessible sections
- **Authorization**: Requires valid JWT token (any authenticated user)
- **Response Fields**:
  - `role`: Current user's role (superuser, admin, user)
  - `can_access_admin`: Boolean indicating admin access
  - `sections`: Array of accessible plugin sections

#### GET /api/v1/users/plugins/access/{section}
- **Purpose**: Check access to specific plugin section
- **Method**: GET
- **Path Parameter**: `section` (string)
- **Response**: Access decision with section name and permission status
- **Authorization**: Requires valid JWT token (any authenticated user)
- **Response Fields**:
  - `section`: Requested section name
  - `has_access`: Boolean indicating access permission
  - `role`: Current user's role

#### GET /api/v1/users/
- **Purpose**: Retrieve paginated list of users
- **Method**: GET
- **Response**: Array of UserResponse objects
- **Parameters**: 
  - `skip`: Integer offset for pagination (default: 0)
  - `limit`: Integer maximum results (default: 100)
- **Authorization**: Requires superuser role

#### GET /api/v1/users/{user_id}
- **Purpose**: Retrieve specific user by ID
- **Method**: GET
- **Path Parameter**: `user_id` (integer)
- **Response**: UserResponse object
- **Authorization**: 
  - Superuser: Full access to any user
  - Regular users: Can only access their own profile

#### POST /api/v1/users/
- **Purpose**: Create new user account
- **Method**: POST
- **Request Body**: UserCreate schema
- **Response**: UserResponse object
- **Authorization**: Requires superuser role
- **Restrictions**: Cannot create superuser accounts

#### PUT /api/v1/users/{user_id}
- **Purpose**: Update existing user
- **Method**: PUT
- **Path Parameter**: `user_id` (integer)
- **Request Body**: UserUpdate schema (partial updates)
- **Response**: UserResponse object
- **Authorization**: Requires superuser role
- **Restrictions**: Cannot assign superuser role without superuser privileges

#### DELETE /api/v1/users/{user_id}
- **Purpose**: Remove user account
- **Method**: DELETE
- **Path Parameter**: `user_id` (integer)
- **Response**: StatusResponse object
- **Authorization**: Requires superuser role
- **Restrictions**: Cannot delete own account, cannot delete last superuser

**Section sources**
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)
- [users.py:38-49](file://backend/app/api/v1/endpoints/users.py#L38-L49)
- [users.py:49-72](file://backend/app/api/v1/endpoints/users.py#L49-L72)
- [users.py:50-62](file://backend/app/api/v1/endpoints/users.py#L50-L62)
- [users.py:15-22](file://backend/app/api/v1/endpoints/users.py#L15-L22)
- [users.py:74-86](file://backend/app/api/v1/endpoints/users.py#L74-L86)
- [users.py:88-97](file://backend/app/api/v1/endpoints/users.py#L88-L97)
- [users.py:99-113](file://backend/app/api/v1/endpoints/users.py#L99-L113)
- [users.py:115-140](file://backend/app/api/v1/endpoints/users.py#L115-L140)
- [users.py:141-164](file://backend/app/api/v1/endpoints/users.py#L141-L164)
- [users.py:166-187](file://backend/app/api/v1/endpoints/users.py#L166-L187)

### Request/Response Schemas

#### UserCreate Schema
Fields for user registration and creation:
- `username`: String (required)
- `email`: String (required)
- `password`: String (required)
- `full_name`: String (optional)
- `role`: String (default: "user")

Validation rules:
- Username must be unique
- Email must be unique
- Password must meet security requirements
- Role must be either "superuser", "admin", or "user"
- Superusers can only be created by other superusers

#### UserUpdate Schema
Fields for partial user updates:
- `email`: String (optional)
- `full_name`: String (optional)
- `role`: String (optional)
- `is_active`: Boolean (optional)
- `password`: String (optional)
- `avatar_url`: String (optional)
- `background_image`: String (optional)
- `theme`: String (optional, default: "light")

Behavior:
- Only provided fields are updated
- Password updates trigger re-hashing
- Role changes require superuser privileges
- Cannot assign superuser role without superuser privileges
- **Updated**: Theme field for color theme preferences (light, dark, system)
- **Updated**: Avatar URL updates for profile customization
- **Updated**: Background image updates for desktop customization

#### UserResponse Schema
Complete user profile representation:
- `id`: Integer (auto-generated)
- `username`: String
- `email`: String
- `full_name`: String (nullable)
- `role`: String ("superuser", "admin", or "user")
- `avatar_url`: String (nullable)
- `background_image`: String (nullable)
- `theme`: String (nullable, default: "light")
- `is_active`: Boolean
- `created_at`: DateTime (nullable)
- `updated_at`: DateTime (nullable)

#### StatusResponse Schema
Standard response for deletion operations:
- `status`: String ("ok")
- `message`: String (optional)

#### PermissionResponse Schema
Permission information for current user:
- `role`: String (current user's role)
- `can_access_admin`: Boolean (indicates admin access capability)
- `sections`: Array of strings (accessible plugin sections)

#### BackgroundsListResponse Schema
Available background images list:
- `backgrounds`: Array of strings (available background image filenames)

**Section sources**
- [user.py:6-11](file://backend/app/schemas/user.py#L6-L11)
- [user.py:14-19](file://backend/app/schemas/user.py#L14-L19)
- [user.py:22-32](file://backend/app/schemas/user.py#L22-L32)
- [common.py:5-7](file://backend/app/schemas/common.py#L5-L7)

### Unified Profile Update Functionality

#### PUT /api/v1/users/me Endpoint
The new unified profile update endpoint provides comprehensive user profile management in a single operation:

##### Allowed Fields
The endpoint processes only the following allowed fields:
- `theme`: Color theme preference (light, dark, system)
- `background_image`: Background image filename or null to clear
- `full_name`: User's full name
- `email`: User's email address
- `avatar_url`: Avatar URL or system avatar format
- `password`: New password (hashed automatically)

##### Field Processing Logic
```mermaid
flowchart TD
Start([Profile Update Request]) --> Extract["Extract UserUpdate Data"]
Extract --> Filter["Filter Allowed Fields"]
Filter --> CheckPassword{"Password Provided?"}
CheckPassword --> |Yes| Hash["Hash New Password"]
CheckPassword --> |No| Skip["Skip Password Update"]
Hash --> SetFields["Set Allowed Fields"]
Skip --> SetFields
SetFields --> ClearNulls["Clear Null Fields"]
ClearNulls --> UpdateDB["Update Database"]
UpdateDB --> Return["Return Updated User"]
```

**Diagram sources**
- [users.py:50-62](file://backend/app/api/v1/endpoints/users.py#L50-L62)
- [user_service.py:46-58](file://backend/app/services/user_service.py#L46-L58)

##### Frontend Integration
The frontend integrates with the unified endpoint through:
- Theme store synchronization with user profile
- Background image management with automatic saving
- Real-time profile updates without page reload
- Consistent user experience across all profile settings

**Section sources**
- [users.py:50-62](file://backend/app/api/v1/endpoints/users.py#L50-L62)
- [Display.vue:35-51](file://frontend/src/views/settings/Display.vue#L35-L51)
- [theme.js:74-86](file://frontend/src/stores/theme.js#L74-L86)

### Background Management Functionality

#### Background Image Management
The system provides comprehensive background image management for user desktop customization:

##### Background Image Storage
- Database field: `background_image` (String, max 255 characters)
- Nullable field allowing empty/null values for default backgrounds
- Stored as filename strings (e.g., "bg1.jpg", "nature.png")

##### Background Image Retrieval
The system searches for available background images in the following order:
1. **Production Environment**: `/usr/share/nginx/html/backgrounds` (nginx static directory)
2. **Development Environment**: `frontend/public/backgrounds` (local development directory)
3. **Fallback**: Returns empty array if neither directory exists

Supported file formats:
- JPEG/JPG
- PNG
- WebP
- GIF
- AVIF

##### Background Image Validation
- Background images must be valid filenames from the available backgrounds list
- Empty/null values indicate default background behavior
- Filename length limited to 255 characters

#### Frontend Integration
The frontend provides comprehensive background management:
- Dynamic background image loading from static asset directories
- Background selection interface with thumbnail previews
- Real-time background preview before saving
- Responsive background management component

**Section sources**
- [user.py:15-16](file://backend/app/models/user.py#L15-L16)
- [user.py:29-32](file://backend/app/models/user.py#L29-L32)
- [user.py:19-20](file://backend/app/schemas/user.py#L19-L20)
- [user.py:28-29](file://backend/app/schemas/user.py#L28-L29)
- [users.py:49-72](file://backend/app/api/v1/endpoints/users.py#L49-L72)
- [002_add_background_image_to_users.py:21-22](file://backend/alembic/versions/002_add_background_image_to_users.py#L21-L22)

### Avatar Management Functionality

#### Avatar URL Formats
The system supports two types of avatar URLs:
- **Custom URLs**: Full URL to external image (e.g., "https://example.com/avatar.jpg")
- **System Avatars**: Predefined system avatars with format "system:n" where n is 1, 2, or 3

#### Avatar Validation Rules
- Custom URLs must be valid HTTP/HTTPS URLs
- System avatars must match format "system:1", "system:2", or "system:3"
- Avatar URLs are optional during user creation/update
- Empty avatar_url indicates default initials avatar

#### Frontend Integration
The frontend provides comprehensive avatar management:
- System avatar selection with predefined SVG images
- Custom image upload with preview functionality
- Real-time avatar preview before saving
- Responsive avatar component with fallback initials

**Section sources**
- [user.py:15-16](file://backend/app/models/user.py#L15-L16)
- [user.py:29-32](file://backend/app/models/user.py#L29-L32)
- [user.py:19-20](file://backend/app/schemas/user.py#L19-L20)
- [user.py:28-29](file://backend/app/schemas/user.py#L28-L29)
- [Profile.vue:18-23](file://frontend/src/views/settings/Profile.vue#L18-L23)
- [Profile.vue:46-57](file://frontend/src/views/settings/Profile.vue#L46-L57)

### Theme Preferences Management

#### Theme Field Implementation
The system provides comprehensive theme preferences for user interface customization:

##### Theme Values
- `light`: Light color scheme
- `dark`: Dark color scheme  
- `system`: Follow system color scheme preference

##### Theme Storage
- Database field: `theme` (String, max 20 characters)
- Nullable field with default value "light"
- Stored as string values for easy processing

##### Theme Synchronization
The theme system synchronizes across:
- Backend user profile storage
- Frontend theme store state
- Real-time UI updates without page reload
- System theme detection and follow-up

##### Frontend Integration
The theme store provides:
- Automatic theme detection based on system preferences
- Real-time theme switching with immediate UI updates
- Persistent theme preferences synchronized with user profile
- Responsive theme application across all components

**Section sources**
- [user.py:17-18](file://backend/app/models/user.py#L17-L18)
- [user.py:32-33](file://backend/app/models/user.py#L32-L33)
- [user.py:21-22](file://backend/app/schemas/user.py#L21-L22)
- [user.py:34-35](file://backend/app/schemas/user.py#L34-L35)
- [Display.vue:35-51](file://frontend/src/views/settings/Display.vue#L35-L51)
- [theme.js:74-86](file://frontend/src/stores/theme.js#L74-L86)

### Authorization Requirements and Role-Based Access Control

#### Authentication Flow
All user management endpoints require valid JWT authentication:
- Token type: Bearer
- Token source: OAuth2 password flow
- Token validation: JWT decoding with secret key
- Expiration handling: Automatic validation

#### Enhanced Role-Based Access Control Matrix
| Endpoint | Required Role | Additional Restrictions |
|----------|---------------|------------------------|
| PUT /users/me | Any authenticated user | N/A |
| PUT /users/me/avatar | Any authenticated user | N/A |
| PUT /users/me/background | Any authenticated user | N/A |
| GET /users/me/backgrounds-list | Any authenticated user | N/A |
| GET /users/me/permissions | Any authenticated user | N/A |
| GET /users/plugins/access/{section} | Any authenticated user | N/A |
| GET /users | Superuser | N/A |
| GET /users/{id} | Superuser or self | Self-access only for non-superusers |
| POST /users | Superuser | Cannot create superuser |
| PUT /users/{id} | Superuser | Cannot assign superuser without superuser |
| DELETE /users/{id} | Superuser | Cannot delete self, cannot delete last superuser |

#### Enhanced Permission Validation Logic
```mermaid
flowchart TD
Start([Request Received]) --> Auth["Validate JWT Token"]
Auth --> CheckActive{"User Active?"}
CheckActive --> |No| Forbidden["HTTP 403 Forbidden"]
CheckActive --> |Yes| CheckRole{"Required Role?"}
CheckRole --> |Superuser| CheckLastSuperuser{"Last Superuser?"}
CheckRole --> |Admin| CheckAdmin["Admin Access"]
CheckRole --> |User| CheckSelf{"Accessing Self?"}
CheckLastSuperuser --> |Yes| CheckSelf
CheckLastSuperuser --> |No| CheckUnified{"Unified Update?"}
CheckSelf --> |Yes| CheckUnified
CheckSelf --> |No| Forbidden
CheckUnified --> |Yes| CheckAllowed{"Allowed Field?"}
CheckUnified --> |No| CheckUserOp{"User Operation?"}
CheckAllowed --> |Yes| Proceed["Proceed to Update"]
CheckAllowed --> |No| Forbidden
CheckUserOp --> |Yes| CheckPrivileges["Check Privileges"]
CheckUserOp --> |No| Proceed
CheckPrivileges --> |Sufficient| Proceed
CheckPrivileges --> |Insufficient| Forbidden
CheckAdmin --> |Yes| Proceed
CheckAdmin --> |No| Forbidden
Proceed --> End([Response Sent])
Forbidden --> End
```

**Diagram sources**
- [security.py:101-110](file://backend/app/core/security.py#L101-L110)
- [users.py:110-115](file://backend/app/api/v1/endpoints/users.py#L110-L115)

**Section sources**
- [security.py:101-110](file://backend/app/core/security.py#L101-L110)
- [users.py:110-115](file://backend/app/api/v1/endpoints/users.py#L110-L115)

### Plugin Access Control

#### Plugin Section Access Validation
The system provides granular access control for different plugin sections based on user roles:

| Role | Accessible Sections |
|------|-------------------|
| Superuser | operations, analytics, security, admin |
| User | operations, general |

#### Access Control Logic
```mermaid
flowchart TD
Start([Plugin Access Request]) --> GetUserRole["Get User Role"]
GetUserRole --> CheckSuperuser{"Is Superuser?"}
CheckSuperuser --> |Yes| AllowAll["Allow All Sections"]
CheckSuperuser --> |No| CheckUserRole{"User Role?"}
CheckUserRole --> |User| CheckAllowed{"Section Allowed?"}
CheckUserRole --> |Other| Deny["Deny Access"]
CheckAllowed --> |Yes| Allow["Allow Access"]
CheckAllowed --> |No| Deny
AllowAll --> End([Access Granted])
Allow --> End
Deny --> End
```

**Diagram sources**
- [security.py:113-133](file://backend/app/core/security.py#L113-L133)

**Section sources**
- [security.py:113-133](file://backend/app/core/security.py#L113-L133)

### Data Validation and Security Considerations

#### Password Management
- Password hashing: bcrypt with salt generation
- Password verification: bcrypt.checkpw comparison
- Password updates: Automatic re-hashing on change
- Storage: Only hashed passwords stored

#### Enhanced Input Validation
- Email format validation using EmailStr
- Unique constraint enforcement (username, email)
- Role validation against allowed values ("superuser", "admin", "user")
- Type validation through Pydantic models
- Superuser privilege validation for role assignments
- **Updated**: Avatar URL validation for custom URLs and system avatar formats
- **Updated**: Background image validation for valid filenames and supported formats
- **Updated**: Theme validation for allowed values (light, dark, system)

#### Enhanced Security Measures
- JWT token expiration (configurable)
- Token revocation on logout
- SQL injection prevention through ORM
- CSRF protection via token-based auth
- Superuser-only access for critical operations
- Prevention of last superuser removal
- Plugin access control enforcement
- **Updated**: Avatar URL validation and sanitization
- **Updated**: Background image filename validation and path safety
- **Updated**: Theme field validation and sanitization

**Section sources**
- [security.py:16-28](file://backend/app/core/security.py#L16-L28)
- [user_service.py:46-58](file://backend/app/services/user_service.py#L46-L58)

### Practical Usage Examples

#### Unified Profile Update Examples

##### Update Theme Preference
```javascript
// PUT /api/v1/users/me
const updateTheme = {
  theme: "dark"
};
```

##### Update Multiple Profile Fields
```javascript
// PUT /api/v1/users/me
const updateProfile = {
  theme: "system",
  background_image: "nature_001.jpg",
  full_name: "John Smith",
  email: "john.smith@example.com"
  // password field omitted for partial update
};
```

##### Clear Background Preference
```javascript
// PUT /api/v1/users/me
const clearBackground = {
  background_image: null
};
```

#### Avatar Management Examples

##### Update User Avatar with Custom URL
```javascript
// PUT /api/v1/users/me/avatar
const updateAvatar = {
  avatar_url: "https://example.com/custom-avatar.jpg"
};
```

##### Update User Avatar with System Avatar
```javascript
// PUT /api/v1/users/me/avatar
const updateAvatar = {
  avatar_url: "system:2"
};
```

##### User Creation with Avatar
```javascript
// POST /api/v1/users/
const createUser = {
  username: "john_doe",
  email: "john@example.com",
  password: "SecurePass123!",
  full_name: "John Doe",
  role: "user",
  avatar_url: "system:1"
};
```

#### Background Management Examples

##### Update User Background
```javascript
// PUT /api/v1/users/me/background
const updateBackground = {
  background_image: "nature_001.jpg"
};
```

##### Get Available Backgrounds
```javascript
// GET /api/v1/users/me/backgrounds-list
{
  "backgrounds": ["nature_001.jpg", "abstract_002.png", "cityscape_003.webp"]
}
```

##### User Creation with Background
```javascript
// POST /api/v1/users/
const createUser = {
  username: "john_doe",
  email: "john@example.com",
  password: "SecurePass123!",
  full_name: "John Doe",
  role: "user",
  background_image: "default_bg.jpg"
};
```

#### Permission Check Example
```javascript
// GET /api/v1/users/me/permissions
{
  "role": "user",
  "can_access_admin": false,
  "sections": ["operations"]
}

// GET /api/v1/users/plugins/access/analytics
{
  "section": "analytics",
  "has_access": false,
  "role": "user"
}
```

#### User Update Example
```javascript
// PUT /api/v1/users/123
const updateUser = {
  email: "newemail@example.com",
  full_name: "John Smith",
  background_image: "modern_001.png"
  // avatar_url field omitted for partial update
};
```

#### Bulk Operations
While individual endpoints support bulk operations, the current implementation focuses on single-user operations. For bulk operations, consider:
- Batch processing in client applications
- Implementing dedicated bulk endpoints
- Using transactional operations for consistency

#### User Search and Filtering
Current implementation supports:
- Pagination via skip/limit parameters
- Individual user retrieval by ID
- No built-in filtering capabilities

Future enhancements could include:
- Query parameters for filtering by role, status, avatar type, background type, theme
- Sorting options (created_at, username)
- Advanced search operators

**Section sources**
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)
- [users.py:38-49](file://backend/app/api/v1/endpoints/users.py#L38-L49)
- [users.py:49-72](file://backend/app/api/v1/endpoints/users.py#L49-L72)
- [users.py:50-62](file://backend/app/api/v1/endpoints/users.py#L50-L62)
- [users.py:17-18](file://backend/app/api/v1/endpoints/users.py#L17-L18)
- [users.py:40-47](file://backend/app/api/v1/endpoints/users.py#L40-L47)
- [users.py:50-71](file://backend/app/api/v1/endpoints/users.py#L50-L71)
- [users.py:40-57](file://backend/app/api/v1/endpoints/users.py#L40-L57)

## Dependency Analysis

```mermaid
graph TB
subgraph "API Layer"
UsersEndpoint["Users Endpoint"]
AuthEndpoint["Auth Endpoint"]
UnifiedEndpoint["Unified Profile Update"]
End
subgraph "Service Layer"
UserService["User Service"]
AuthService["Auth Service"]
End
subgraph "Data Layer"
UserModel["User Model"]
DB["Database"]
End
subgraph "Security Layer"
SecurityUtils["Security Utilities"]
JWT["JWT Handler"]
PluginAccess["Plugin Access Control"]
End
subgraph "Frontend Layer"
AvatarComponent["Avatar Component"]
ProfileView["Profile View"]
AuthStore["Auth Store"]
BackgroundComponent["Background Component"]
ThemeStore["Theme Store"]
End
UsersEndpoint --> UserService
AuthEndpoint --> AuthService
UnifiedEndpoint --> UserService
UserService --> UserModel
AuthService --> UserModel
UsersEndpoint --> SecurityUtils
AuthEndpoint --> SecurityUtils
SecurityUtils --> JWT
SecurityUtils --> PluginAccess
UserModel --> DB
AvatarComponent --> ProfileView
BackgroundComponent --> ProfileView
ThemeStore --> UnifiedEndpoint
ProfileView --> AuthStore
```

**Diagram sources**
- [users.py:10](file://backend/app/api/v1/endpoints/users.py#L10)
- [auth.py:15](file://backend/app/api/v1/endpoints/auth.py#L15)
- [user_service.py:4](file://backend/app/services/user_service.py#L4)
- [security.py:13](file://backend/app/core/security.py#L13)
- [Avatar.vue:1-58](file://frontend/src/components/ui/Avatar.vue#L1-L58)
- [Profile.vue:1-199](file://frontend/src/views/settings/Profile.vue#L1-L199)
- [Display.vue:1-202](file://frontend/src/views/settings/Display.vue#L1-L202)
- [theme.js:1-104](file://frontend/src/stores/theme.js#L1-L104)
- [auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)

Key dependencies:
- SQLAlchemy ORM for database operations
- Pydantic for request/response validation
- bcrypt for password hashing
- JWT library for token management
- FastAPI for routing and dependency injection
- Enhanced security utilities for role-based access control
- **Updated**: Frontend avatar component integration
- **Updated**: Background image management integration
- **Updated**: Theme preferences store integration
- **Updated**: Unified profile update endpoint integration

**Section sources**
- [users.py:1-10](file://backend/app/api/v1/endpoints/users.py#L1-L10)
- [user_service.py:1-5](file://backend/app/services/user_service.py#L1-L5)

## Performance Considerations
- Pagination limits: Default limit of 100 users prevents excessive memory usage
- Database indexing: Username and email fields are indexed for efficient lookups
- Lazy loading: Relationship loading follows SQLAlchemy best practices
- Token caching: JWT validation results could benefit from caching layer
- Connection pooling: SQLAlchemy session management handles connection reuse
- Superuser count checks: Efficient database queries prevent orphan superuser scenarios
- **Updated**: Avatar URL storage optimization for minimal database overhead
- **Updated**: Background image filename storage optimization for minimal database overhead
- **Updated**: Theme field storage optimization for minimal database overhead
- **Updated**: Background directory scanning optimized with early termination on first found directory
- **Updated**: Unified profile update endpoint reduces multiple API calls for comprehensive updates

## Troubleshooting Guide

### Common Error Scenarios
- **401 Unauthorized**: Invalid or missing JWT token
- **403 Forbidden**: Insufficient permissions, inactive user, or superuser-only access
- **404 Not Found**: User does not exist
- **400 Bad Request**: Duplicate username/email, self-deletion attempt, last superuser removal, invalid avatar URL format, invalid background image filename, or invalid theme value

### Authentication Issues
- Verify token format: Must be Bearer token
- Check token expiration: Tokens have configurable expiry
- Validate user status: Only active users can access endpoints
- Confirm role assignment: Superuser privileges required for user management

### Data Validation Errors
- Username uniqueness: Ensure username is not already taken
- Email uniqueness: Verify email address availability
- Password requirements: Meet security criteria
- Role validation: Only "superuser", "admin", or "user" roles allowed
- Superuser validation: Ensure proper privilege escalation
- **Updated**: Avatar URL validation: Ensure valid URL format or system avatar format
- **Updated**: Background image validation: Ensure filename exists in available backgrounds list
- **Updated**: Theme validation: Ensure theme is one of "light", "dark", or "system"

### Permission Issues
- Check user role: Verify current user has appropriate permissions
- Plugin access: Ensure requested section is accessible
- Superuser restrictions: Some operations are restricted to superusers only
- **Updated**: Unified update restrictions: Only allowed fields can be updated
- **Updated**: Avatar updates: Any authenticated user can update their own avatar
- **Updated**: Background updates: Any authenticated user can update their own background preferences
- **Updated**: Theme updates: Any authenticated user can update their own theme preference

### Unified Profile Update Issues
- **Field Not Allowed**: Only theme, background_image, full_name, email, avatar_url, password are allowed
- **Password Hashing**: Password updates are automatically hashed, cannot be retrieved in plain text
- **Partial Updates**: Only provided fields are updated, others remain unchanged
- **Theme Validation**: Ensure theme value is one of "light", "dark", or "system"

### Avatar Management Issues
- **Invalid Avatar URL**: Ensure URL is valid HTTP/HTTPS or follows system avatar format
- **System Avatar Error**: Use format "system:1", "system:2", or "system:3"
- **File Upload Issues**: Frontend handles local file uploads, server expects URL string
- **Avatar Preview**: System avatars use predefined SVG files, custom avatars use uploaded URLs

### Background Management Issues
- **Background Directory Missing**: Production environment may not have nginx static directory mounted
- **Invalid Background Filename**: Ensure filename exists in the backgrounds-list response
- **File Format Not Supported**: Only jpg, jpeg, png, webp, gif, avif formats supported
- **Background Preview Issues**: Check that background files are accessible from static directory
- **Development vs Production**: Backgrounds-list searches different paths in development vs production environments

### Theme Preferences Issues
- **Invalid Theme Value**: Ensure theme is one of "light", "dark", or "system"
- **Theme Synchronization**: Theme changes are immediately reflected in UI but may take time to sync with user profile
- **System Theme Detection**: System theme follows OS preferences, requires browser support for prefers-color-scheme

**Section sources**
- [users.py:32-36](file://backend/app/api/v1/endpoints/users.py#L32-L36)
- [users.py:46-49](file://backend/app/api/v1/endpoints/users.py#L46-L49)
- [users.py:79-80](file://backend/app/api/v1/endpoints/users.py#L79-L80)
- [users.py:49-72](file://backend/app/api/v1/endpoints/users.py#L49-L72)
- [users.py:50-62](file://backend/app/api/v1/endpoints/users.py#L50-L62)

## Conclusion
The user management endpoints provide a robust foundation for user lifecycle operations within the NOC Vision platform. The implementation emphasizes security through JWT authentication, enhanced role-based access control with superuser privileges, and comprehensive data validation. The addition of new permission endpoints, plugin access control, avatar management functionality, background management functionality, and unified profile update capabilities provides comprehensive user profile customization and management capabilities.

The new unified PUT /api/v1/users/me endpoint represents a significant enhancement to the user management system, consolidating multiple profile update operations into a single, comprehensive endpoint. This endpoint allows users to update theme preferences, background images, avatar URLs, email addresses, full names, and passwords in a single request, reducing API complexity and improving user experience.

The system intelligently manages user preferences by storing theme settings, background images, and avatar URLs in the database while providing real-time synchronization with the frontend theme store. The unified endpoint processes only allowed fields, ensuring data integrity and preventing unauthorized modifications to protected user attributes.

The enhanced UserUpdate schema now includes theme field support with validation for "light", "dark", or "system" values, while the UserResponse schema provides complete profile information including all customizable fields. The database model has been extended to support theme preferences alongside existing avatar and background image fields.

The frontend integration provides seamless user experience through the theme store, background management components, and unified profile update functionality. Users can now manage all their profile preferences through a single endpoint while maintaining the security and validation benefits of the existing system architecture.

The current implementation focuses on individual user operations with enhanced security measures, including prevention of last superuser removal, proper privilege escalation, avatar URL validation, background image filename validation, theme field validation, and comprehensive input sanitization. The modular design ensures maintainability and extensibility for evolving user management requirements, with clear separation between user management, authentication, permission control, avatar management, background management, and unified profile update functionality.