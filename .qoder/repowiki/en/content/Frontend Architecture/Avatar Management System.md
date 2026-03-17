# Avatar Management System

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [main.py](file://backend/app/main.py)
- [router.py](file://backend/app/api/v1/router.py)
- [users.py](file://backend/app/api/v1/endpoints/users.py)
- [user.py](file://backend/app/models/user.py)
- [user.py](file://backend/app/schemas/user.py)
- [user_service.py](file://backend/app/services/user_service.py)
- [security.py](file://backend/app/core/security.py)
- [Avatar.vue](file://frontend/src/components/ui/Avatar.vue)
- [auth.js](file://frontend/src/stores/auth.js)
- [Profile.vue](file://frontend/src/views/settings/Profile.vue)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Avatar Management Components](#avatar-management-components)
4. [Backend Implementation](#backend-implementation)
5. [Frontend Implementation](#frontend-implementation)
6. [Data Flow Analysis](#data-flow-analysis)
7. [Security Considerations](#security-considerations)
8. [Configuration and Setup](#configuration-and-setup)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Conclusion](#conclusion)

## Introduction

The Avatar Management System is a core feature of the NOC Vision Network Operations Center Platform, providing users with the ability to customize their profile appearance through personalized avatars. This system integrates seamlessly with the existing authentication and user management infrastructure, offering both system-generated avatars and custom image uploads.

The platform supports three distinct avatar types:
- **System Avatars**: Predefined SVG images with identifiers like `system:1`, `system:2`, `system:3`
- **Custom Uploads**: User-uploaded images stored as URLs
- **Fallback Initials**: Generated from user's full name or username

Built with a modern tech stack featuring FastAPI backend and Vue 3 frontend, the system ensures secure, scalable avatar management with robust validation and error handling mechanisms.

## System Architecture

The Avatar Management System follows a distributed architecture pattern with clear separation of concerns between frontend presentation, backend business logic, and database persistence.

```mermaid
graph TB
subgraph "Frontend Layer"
UI[Vue 3 Components]
Store[Pinia State Management]
AvatarComp[Avatar Component]
ProfileView[Profile Settings View]
end
subgraph "Backend Layer"
API[FastAPI Router]
UsersEndpoint[Users Endpoint]
UserService[User Service]
Security[Security Middleware]
end
subgraph "Data Layer"
UserModel[User Model]
Database[(PostgreSQL Database)]
end
subgraph "External Resources"
SystemAvatars[System Avatars Directory]
UploadStorage[Image Upload Storage]
end
UI --> Store
Store --> AvatarComp
Store --> ProfileView
ProfileView --> API
API --> UsersEndpoint
UsersEndpoint --> UserService
UsersEndpoint --> Security
UserService --> UserModel
UserModel --> Database
AvatarComp --> SystemAvatars
ProfileView --> UploadStorage
```

**Diagram sources**
- [main.py:50-87](file://backend/app/main.py#L50-L87)
- [router.py:1-10](file://backend/app/api/v1/router.py#L1-L10)
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)

## Avatar Management Components

### Backend Components

The backend implementation consists of several interconnected components working together to provide comprehensive avatar management functionality.

#### User Model Enhancement
The User model has been extended to include avatar_url field supporting multiple avatar types:
- **System avatars**: Stored as `system:{id}` format
- **Custom URLs**: Direct image URLs
- **Null values**: Fallback to initials generation

#### API Endpoints
The `/api/v1/users/me/avatar` endpoint provides secure avatar update functionality with proper authentication and authorization checks.

#### Service Layer
The user service handles avatar-specific operations while maintaining consistency with existing user management workflows.

### Frontend Components

The frontend implementation provides an intuitive user interface for avatar selection and management.

#### Avatar Component
A reusable Vue component supporting different sizing options and fallback mechanisms for displaying user avatars.

#### Profile Settings Interface
A comprehensive settings page allowing users to choose between system avatars, upload custom images, or use generated initials.

**Section sources**
- [user.py:16](file://backend/app/models/user.py#L16)
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)
- [Avatar.vue:1-58](file://frontend/src/components/ui/Avatar.vue#L1-L58)

## Backend Implementation

### Database Schema

The User model includes an avatar_url column designed to accommodate various avatar storage strategies:

```mermaid
erDiagram
USER {
integer id PK
string username UK
string email UK
string full_name
string hashed_password
string role
string avatar_url
boolean is_active
timestamp created_at
timestamp updated_at
}
```

**Diagram sources**
- [user.py:7-37](file://backend/app/models/user.py#L7-L37)

### API Endpoint Implementation

The avatar management endpoint follows RESTful principles with comprehensive error handling and validation:

```mermaid
sequenceDiagram
participant Client as "Frontend Client"
participant API as "Users Endpoint"
participant Service as "User Service"
participant DB as "Database"
Client->>API : PUT /api/v1/users/me/avatar
API->>API : Validate Authentication
API->>API : Extract avatar_url from request
API->>Service : update_user(db, current_user, avatar_url)
Service->>DB : Update user.avatar_url
DB-->>Service : Updated user record
Service-->>API : UserResponse
API-->>Client : Updated avatar information
```

**Diagram sources**
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)
- [user_service.py:46-58](file://backend/app/services/user_service.py#L46-L58)

### Security Implementation

The system implements robust security measures including:

- **Authentication**: JWT-based authentication with access and refresh tokens
- **Authorization**: Role-based access control ensuring users can only modify their own avatar
- **Input Validation**: Comprehensive validation of avatar URLs and system avatar identifiers
- **Password Security**: bcrypt hashing for password protection

**Section sources**
- [security.py:61-110](file://backend/app/core/security.py#L61-L110)
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)

## Frontend Implementation

### Avatar Component Architecture

The frontend avatar component provides flexible sizing and fallback capabilities:

```mermaid
classDiagram
class AvatarComponent {
+String src
+String alt
+String fallback
+String size
+String class
+Map~String,String~ sizeClasses
+computed initials
+render() Template
}
class SizeClasses {
+String sm
+String md
+String lg
}
class AvatarComponent {
+sizeClasses Map~String,String~
+initials ComputedRef
+render() Template
}
AvatarComponent --> SizeClasses : uses
```

**Diagram sources**
- [Avatar.vue:1-58](file://frontend/src/components/ui/Avatar.vue#L1-L58)

### Profile Settings Integration

The Profile.vue component integrates avatar management with the broader user settings interface:

```mermaid
flowchart TD
Start([User Opens Profile Settings]) --> LoadAvatar["Load Current Avatar"]
LoadAvatar --> CheckType{"Avatar Type?"}
CheckType --> |System Avatar| ShowSystem["Display System Avatar"]
CheckType --> |Custom URL| ShowCustom["Display Custom Image"]
CheckType --> |No Avatar| ShowInitials["Generate Initials"]
ShowSystem --> SelectOption["User Selects Option"]
ShowCustom --> SelectOption
ShowInitials --> SelectOption
SelectOption --> SystemAvatars["Select System Avatar"]
SelectOption --> UploadImage["Upload Custom Image"]
SystemAvatars --> Preview["Preview Selection"]
UploadImage --> Preview
Preview --> SaveChanges["Save Avatar Changes"]
SaveChanges --> UpdateAPI["Call /api/v1/users/me/avatar"]
UpdateAPI --> UpdateLocal["Update Local State"]
UpdateLocal --> Success["Show Success Message"]
```

**Diagram sources**
- [Profile.vue:59-80](file://frontend/src/views/settings/Profile.vue#L59-L80)
- [auth.js:160-177](file://frontend/src/stores/auth.js#L160-L177)

### State Management

The Pinia store manages authentication state and provides centralized access to avatar-related functionality:

- **Authentication State**: Token management, user data persistence
- **Avatar State**: Current avatar selection, loading states
- **Error Handling**: Comprehensive error management for avatar operations

**Section sources**
- [auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)
- [Profile.vue:1-199](file://frontend/src/views/settings/Profile.vue#L1-L199)

## Data Flow Analysis

### Avatar Update Process

The avatar update process involves multiple validation steps and state synchronization:

```mermaid
sequenceDiagram
participant User as "User Action"
participant Profile as "Profile Component"
participant Store as "Auth Store"
participant API as "Backend API"
participant DB as "Database"
User->>Profile : Select Avatar Option
Profile->>Profile : Validate Selection
Profile->>Store : Call authFetch()
Store->>API : PUT /api/v1/users/me/avatar
API->>API : Authenticate Request
API->>API : Validate Avatar Data
API->>DB : Update User Record
DB-->>API : Confirmation
API-->>Store : Success Response
Store-->>Profile : Update Local State
Profile-->>User : Show Success Message
```

**Diagram sources**
- [Profile.vue:64-79](file://frontend/src/views/settings/Profile.vue#L64-L79)
- [users.py:27-35](file://backend/app/api/v1/endpoints/users.py#L27-L35)

### System Avatar Configuration

The system supports predefined avatar sets with automatic fallback mechanisms:

| Avatar Type | Identifier | Storage Location | Fallback Behavior |
|-------------|------------|------------------|-------------------|
| System Avatar | `system:1` | `/avatars/avatar-1.svg` | Uses SVG file |
| System Avatar | `system:2` | `/avatars/avatar-2.svg` | Uses SVG file |
| System Avatar | `system:3` | `/avatars/avatar-3.svg` | Uses SVG file |
| Custom URL | `https://example.com/image.jpg` | External URL | Direct image loading |
| No Avatar | Null | N/A | Generated initials |

**Section sources**
- [Profile.vue:18-23](file://frontend/src/views/settings/Profile.vue#L18-L23)
- [Profile.vue:26-33](file://frontend/src/views/settings/Profile.vue#L26-L33)

## Security Considerations

### Authentication and Authorization

The avatar management system implements multiple layers of security:

- **JWT Authentication**: All avatar operations require valid access tokens
- **User Scope Validation**: Users can only modify their own avatar data
- **Role-Based Permissions**: Enhanced security for administrative operations
- **Input Sanitization**: Validation of avatar URLs and system identifiers

### Data Protection

- **Password Hashing**: bcrypt implementation for password security
- **Token Expiration**: Configurable access and refresh token lifetimes
- **Secure Storage**: Database-level protection for sensitive information
- **CORS Configuration**: Controlled cross-origin resource sharing

### Error Handling and Validation

The system implements comprehensive error handling:
- **Validation Errors**: Proper HTTP status codes for malformed requests
- **Authorization Errors**: Clear 403 responses for unauthorized access
- **Database Errors**: Graceful handling of storage failures
- **Network Errors**: Robust retry mechanisms for API calls

**Section sources**
- [security.py:16-28](file://backend/app/core/security.py#L16-L28)
- [users.py:74-76](file://backend/app/api/v1/endpoints/users.py#L74-L76)

## Configuration and Setup

### Environment Configuration

The system requires minimal configuration for avatar functionality:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/noc_vision

# Security Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Asset Management

System avatars are stored in the public directory:
- `/frontend/public/avatars/avatar-1.svg`
- `/frontend/public/avatars/avatar-2.svg`
- `/frontend/public/avatars/avatar-3.svg`

### Docker Deployment

The system supports containerized deployment with proper volume mounting for avatar storage.

**Section sources**
- [README.md:133-157](file://README.md#L133-L157)

## Troubleshooting Guide

### Common Issues and Solutions

#### Avatar Not Updating
- **Symptoms**: Avatar change appears immediately but reverts after refresh
- **Causes**: Authentication token expiration, network timeout, database write failure
- **Solutions**: Verify token validity, check network connectivity, review backend logs

#### System Avatar Display Issues
- **Symptoms**: System avatars not loading or showing broken images
- **Causes**: Incorrect file paths, missing SVG files, CORS restrictions
- **Solutions**: Verify file existence, check asset paths, configure CORS properly

#### Custom Image Upload Problems
- **Symptoms**: Custom images not saving or displaying incorrectly
- **Causes**: File type restrictions, size limitations, storage permission issues
- **Solutions**: Verify file format support, check size limits, review storage configuration

#### Authentication Failures
- **Symptoms**: Cannot access avatar settings or receive 401 errors
- **Causes**: Expired tokens, invalid credentials, session timeouts
- **Solutions**: Refresh authentication tokens, verify credentials, check token expiration

### Debugging Tools

- **Browser Developer Tools**: Network tab for API request inspection
- **Backend Logs**: Application logs for error tracking and debugging
- **Database Queries**: SQL logs for avatar data verification
- **Authentication Tokens**: JWT decoder for token validation

**Section sources**
- [auth.js:136-158](file://frontend/src/stores/auth.js#L136-L158)
- [users.py:71-76](file://backend/app/api/v1/endpoints/users.py#L71-L76)

## Conclusion

The Avatar Management System represents a well-architected solution that seamlessly integrates with the NOC Vision platform's existing infrastructure. The system successfully balances functionality, security, and user experience through:

- **Robust Architecture**: Clean separation of concerns between frontend and backend
- **Security First Design**: Comprehensive authentication, authorization, and input validation
- **Flexible Implementation**: Support for multiple avatar types with intelligent fallback mechanisms
- **Developer-Friendly Code**: Well-documented APIs, clear component boundaries, and comprehensive error handling

The system's modular design ensures easy maintenance and future enhancements while providing a solid foundation for advanced avatar features such as animated avatars, avatar customization tools, and social avatar integration.

Key strengths include the seamless integration with the existing authentication system, comprehensive error handling, and intuitive user interface that makes avatar management straightforward for end users. The system's extensible architecture also supports future enhancements without requiring significant architectural changes.