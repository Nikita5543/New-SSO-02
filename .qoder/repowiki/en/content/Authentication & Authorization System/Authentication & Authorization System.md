# Authentication & Authorization System

<cite>
**Referenced Files in This Document**
- [backend/app/core/security.py](file://backend/app/core/security.py)
- [backend/app/core/config.py](file://backend/app/core/config.py)
- [backend/app/core/database.py](file://backend/app/core/database.py)
- [backend/app/models/user.py](file://backend/app/models/user.py)
- [backend/app/models/refresh_token.py](file://backend/app/models/refresh_token.py)
- [backend/app/schemas/auth.py](file://backend/app/schemas/auth.py)
- [backend/app/schemas/user.py](file://backend/app/schemas/user.py)
- [backend/app/schemas/common.py](file://backend/app/schemas/common.py)
- [backend/app/services/auth_service.py](file://backend/app/services/auth_service.py)
- [backend/app/services/user_service.py](file://backend/app/services/user_service.py)
- [backend/app/api/v1/endpoints/auth.py](file://backend/app/api/v1/endpoints/auth.py)
- [backend/app/api/v1/router.py](file://backend/app/api/v1/router.py)
- [backend/app/main.py](file://backend/app/main.py)
- [frontend/src/stores/auth.js](file://frontend/src/stores/auth.js)
- [frontend/src/views/auth/SignIn.vue](file://frontend/src/views/auth/SignIn.vue)
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
This document describes the JWT-based authentication and authorization system implemented in the backend and integrated with the frontend. It covers JWT token creation and validation, refresh token rotation, user roles and permissions, password hashing with bcrypt, and security best practices. The document also documents the complete authentication flow from login to token refresh, endpoint specifications, request/response schemas, error handling, and the relationships among the authentication service, user models, and security utilities. Practical examples and security considerations for both backend and frontend implementations are included.

## Project Structure
The authentication system spans several backend modules and integrates with the frontend via a Pinia store and Vue components:
- Backend core: security utilities, configuration, database initialization
- Backend models: user and refresh token persistence
- Backend schemas: request/response models for authentication
- Backend services: authentication and user management logic
- Backend API: authentication endpoints
- Frontend: authentication store and sign-in view

```mermaid
graph TB
subgraph "Backend"
CFG["Config<br/>Security constants"]
SEC["Security Utilities<br/>JWT encode/decode, bcrypt, OAuth2 scheme"]
DB["Database<br/>Engine, Session, Base"]
MDL_USER["User Model"]
MDL_RT["RefreshToken Model"]
SCH_AUTH["Auth Schemas"]
SCH_USER["User Schemas"]
SVC_AUTH["Auth Service"]
SVC_USER["User Service"]
API_AUTH["Auth Endpoints"]
API_ROUTER["API Router"]
MAIN["Main App"]
end
subgraph "Frontend"
FE_STORE["Auth Store<br/>Pinia"]
FE_VIEW["Sign-In View<br/>Vue"]
end
CFG --> SEC
SEC --> API_AUTH
DB --> API_AUTH
DB --> SVC_AUTH
DB --> SVC_USER
MDL_USER --> SVC_AUTH
MDL_RT --> SVC_AUTH
SCH_AUTH --> API_AUTH
SCH_USER --> API_AUTH
SVC_AUTH --> API_AUTH
SVC_USER --> API_AUTH
API_ROUTER --> API_AUTH
MAIN --> API_ROUTER
FE_STORE --> FE_VIEW
FE_STORE --> API_AUTH
```

**Diagram sources**
- [backend/app/core/config.py:1-46](file://backend/app/core/config.py#L1-L46)
- [backend/app/core/security.py:1-99](file://backend/app/core/security.py#L1-L99)
- [backend/app/core/database.py:1-18](file://backend/app/core/database.py#L1-L18)
- [backend/app/models/user.py:1-35](file://backend/app/models/user.py#L1-L35)
- [backend/app/models/refresh_token.py:1-18](file://backend/app/models/refresh_token.py#L1-L18)
- [backend/app/schemas/auth.py:1-26](file://backend/app/schemas/auth.py#L1-L26)
- [backend/app/schemas/user.py:1-33](file://backend/app/schemas/user.py#L1-L33)
- [backend/app/services/auth_service.py:1-139](file://backend/app/services/auth_service.py#L1-L139)
- [backend/app/services/user_service.py:1-69](file://backend/app/services/user_service.py#L1-L69)
- [backend/app/api/v1/endpoints/auth.py:1-106](file://backend/app/api/v1/endpoints/auth.py#L1-L106)
- [backend/app/api/v1/router.py:1-10](file://backend/app/api/v1/router.py#L1-L10)
- [backend/app/main.py:1-87](file://backend/app/main.py#L1-L87)
- [frontend/src/stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)
- [frontend/src/views/auth/SignIn.vue:1-103](file://frontend/src/views/auth/SignIn.vue#L1-L103)

**Section sources**
- [backend/app/main.py:17-48](file://backend/app/main.py#L17-L48)
- [backend/app/api/v1/router.py:1-10](file://backend/app/api/v1/router.py#L1-L10)

## Core Components
- Security utilities: JWT encoding/decoding, bcrypt password hashing/verification, OAuth2 bearer scheme, current user resolution, role-based access checks
- Models: User and RefreshToken tables with relationships
- Schemas: Request/response models for login, token pair, refresh, logout, and user
- Services: Authentication service (token pair creation, refresh with rotation, revocation, cleanup), user service (CRUD and password hashing)
- API endpoints: Login, refresh, register, logout, whoami, admin init
- Frontend store: Authentication state, token lifecycle, protected fetch wrapper

Key implementation references:
- JWT and bcrypt utilities: [backend/app/core/security.py:16-58](file://backend/app/core/security.py#L16-L58)
- Access/refresh token creation: [backend/app/core/security.py:31-48](file://backend/app/core/security.py#L31-L48)
- Current user and role checks: [backend/app/core/security.py:61-98](file://backend/app/core/security.py#L61-L98)
- Token pair creation and DB persistence: [backend/app/services/auth_service.py:19-42](file://backend/app/services/auth_service.py#L19-L42)
- Refresh token rotation and revocation: [backend/app/services/auth_service.py:45-74](file://backend/app/services/auth_service.py#L45-L74)
- User model with role and refresh tokens: [backend/app/models/user.py:7-34](file://backend/app/models/user.py#L7-L34)
- Refresh token model: [backend/app/models/refresh_token.py:7-17](file://backend/app/models/refresh_token.py#L7-L17)
- Auth schemas: [backend/app/schemas/auth.py:5-25](file://backend/app/schemas/auth.py#L5-L25)
- User schemas: [backend/app/schemas/user.py:6-32](file://backend/app/schemas/user.py#L6-L32)
- Auth endpoints: [backend/app/api/v1/endpoints/auth.py:20-105](file://backend/app/api/v1/endpoints/auth.py#L20-L105)
- Frontend auth store: [frontend/src/stores/auth.js:29-177](file://frontend/src/stores/auth.js#L29-L177)

**Section sources**
- [backend/app/core/security.py:16-98](file://backend/app/core/security.py#L16-L98)
- [backend/app/models/user.py:7-34](file://backend/app/models/user.py#L7-L34)
- [backend/app/models/refresh_token.py:7-17](file://backend/app/models/refresh_token.py#L7-L17)
- [backend/app/schemas/auth.py:5-25](file://backend/app/schemas/auth.py#L5-L25)
- [backend/app/schemas/user.py:6-32](file://backend/app/schemas/user.py#L6-L32)
- [backend/app/services/auth_service.py:19-139](file://backend/app/services/auth_service.py#L19-L139)
- [backend/app/api/v1/endpoints/auth.py:20-105](file://backend/app/api/v1/endpoints/auth.py#L20-L105)
- [frontend/src/stores/auth.js:29-177](file://frontend/src/stores/auth.js#L29-L177)

## Architecture Overview
The system follows a layered architecture:
- Presentation layer: FastAPI endpoints under /api/v1/auth
- Service layer: Business logic for authentication and user management
- Persistence layer: SQLAlchemy models for User and RefreshToken
- Security utilities: JWT and bcrypt helpers, OAuth2 bearer scheme
- Frontend integration: Pinia store manages tokens and protected requests

```mermaid
graph TB
CLIENT["Client App"]
AUTH_EP["Auth Endpoints<br/>/api/v1/auth/*"]
AUTH_SVC["Auth Service"]
USER_SVC["User Service"]
SEC_UTIL["Security Utilities"]
DB["Database"]
USER_M["User Model"]
RT_M["RefreshToken Model"]
CLIENT --> AUTH_EP
AUTH_EP --> AUTH_SVC
AUTH_EP --> USER_SVC
AUTH_EP --> SEC_UTIL
AUTH_SVC --> DB
USER_SVC --> DB
SEC_UTIL --> DB
DB --> USER_M
DB --> RT_M
```

**Diagram sources**
- [backend/app/api/v1/endpoints/auth.py:1-106](file://backend/app/api/v1/endpoints/auth.py#L1-L106)
- [backend/app/services/auth_service.py:1-139](file://backend/app/services/auth_service.py#L1-L139)
- [backend/app/services/user_service.py:1-69](file://backend/app/services/user_service.py#L1-L69)
- [backend/app/core/security.py:1-99](file://backend/app/core/security.py#L1-L99)
- [backend/app/models/user.py:1-35](file://backend/app/models/user.py#L1-L35)
- [backend/app/models/refresh_token.py:1-18](file://backend/app/models/refresh_token.py#L1-L18)

## Detailed Component Analysis

### JWT and Password Security Utilities
- Password hashing and verification use bcrypt with salt generation and UTF-8 encoding
- JWT encoding/decoding with HS256 algorithm and configurable secret key
- OAuth2 password bearer scheme pointing to the login endpoint
- Access token carries subject (username) and role; refresh token carries subject and JTI (unique token identifier)
- Token decoding validates algorithm and type ("access" vs "refresh")

```mermaid
flowchart TD
Start(["Token Creation"]) --> BuildClaims["Build Claims<br/>sub, role (access)<br/>sub, jti (refresh)"]
BuildClaims --> SetExp["Set Expiration<br/>ACCESS_TOKEN_EXPIRE_MINUTES<br/>REFRESH_TOKEN_EXPIRE_DAYS"]
SetExp --> Encode["Encode JWT<br/>HS256 with SECRET_KEY"]
Encode --> ReturnTokens["Return Token Pair"]
```

**Diagram sources**
- [backend/app/core/security.py:31-48](file://backend/app/core/security.py#L31-L48)
- [backend/app/core/config.py:9-13](file://backend/app/core/config.py#L9-L13)

**Section sources**
- [backend/app/core/security.py:16-58](file://backend/app/core/security.py#L16-L58)
- [backend/app/core/config.py:9-13](file://backend/app/core/config.py#L9-L13)

### User and Refresh Token Models
- User model includes username, email, full name, hashed password, role, activity status, timestamps, and a relationship to refresh tokens
- RefreshToken model includes unique token (JTI), user foreign key, expiration, revoked flag, and timestamps
- Relationship ensures cascading deletion when a user is removed

```mermaid
erDiagram
USERS {
integer id PK
string username UK
string email UK
string full_name
string hashed_password
string role
boolean is_active
timestamp created_at
timestamp updated_at
}
REFRESH_TOKENS {
integer id PK
string token UK
integer user_id FK
timestamp expires_at
boolean revoked
timestamp created_at
}
USERS ||--o{ REFRESH_TOKENS : "has many"
```

**Diagram sources**
- [backend/app/models/user.py:7-34](file://backend/app/models/user.py#L7-L34)
- [backend/app/models/refresh_token.py:7-17](file://backend/app/models/refresh_token.py#L7-L17)

**Section sources**
- [backend/app/models/user.py:7-34](file://backend/app/models/user.py#L7-L34)
- [backend/app/models/refresh_token.py:7-17](file://backend/app/models/refresh_token.py#L7-L17)

### Authentication Service: Token Pair, Rotation, Revocation
- Creates a token pair with a fresh JTI stored as the refresh token’s unique value
- Stores refresh token metadata with expiration and marks revoked=false
- Refresh flow decodes refresh token, validates JTI and user, checks expiration, revokes old token, and issues a new pair
- Supports revocation by JTI or full token and bulk revocation per user
- Periodic cleanup removes expired refresh tokens

```mermaid
sequenceDiagram
participant C as "Client"
participant EP as "Auth Endpoint"
participant AS as "Auth Service"
participant DB as "Database"
C->>EP : POST /api/v1/auth/login
EP->>AS : authenticate_user(username, password)
AS->>DB : query User
DB-->>AS : User
AS-->>EP : User
EP->>AS : create_token_pair(user)
AS->>DB : persist RefreshToken (jti, expires_at)
DB-->>AS : OK
AS-->>EP : {access_token, refresh_token, user}
EP-->>C : 200 OK {access_token, refresh_token, user}
Note over C,EP : On access token expiration
C->>EP : POST /api/v1/auth/refresh
EP->>AS : refresh_access_token(refresh_token)
AS->>DB : query RefreshToken by jti
DB-->>AS : RefreshToken
AS->>AS : revoke old token
AS->>AS : create_token_pair(user)
AS-->>EP : {access_token, refresh_token, user}
EP-->>C : 200 OK {access_token, refresh_token, user}
```

**Diagram sources**
- [backend/app/api/v1/endpoints/auth.py:20-51](file://backend/app/api/v1/endpoints/auth.py#L20-L51)
- [backend/app/services/auth_service.py:19-74](file://backend/app/services/auth_service.py#L19-L74)
- [backend/app/models/refresh_token.py:7-17](file://backend/app/models/refresh_token.py#L7-L17)

**Section sources**
- [backend/app/services/auth_service.py:19-101](file://backend/app/services/auth_service.py#L19-L101)
- [backend/app/api/v1/endpoints/auth.py:20-51](file://backend/app/api/v1/endpoints/auth.py#L20-L51)

### Role-Based Access Control and Protected Routes
- Current user resolution validates access token and loads the user from the database
- Active user check prevents disabled accounts from accessing protected resources
- Admin-only decorator enforces administrative privileges
- Endpoints decorated with these dependencies enforce authorization policies

```mermaid
flowchart TD
A["Incoming Request"] --> B["OAuth2 Bearer Token"]
B --> C["decode_token()"]
C --> D{"Type == 'access'?"}
D --> |No| E["HTTP 401 Unauthorized"]
D --> |Yes| F["Load User by sub (username)"]
F --> G{"User exists and active?"}
G --> |No| E
G --> |Yes| H["Proceed to Handler"]
H --> I{"Admin Required?"}
I --> |Yes| J{"Role == 'admin'?"}
J --> |No| K["HTTP 403 Forbidden"]
J --> |Yes| L["Allow"]
I --> |No| L
```

**Diagram sources**
- [backend/app/core/security.py:61-98](file://backend/app/core/security.py#L61-L98)

**Section sources**
- [backend/app/core/security.py:61-98](file://backend/app/core/security.py#L61-L98)

### Frontend Authentication Store and Usage
- Maintains access token, refresh token, and expiry timestamp in localStorage
- Provides login, register, logout, whoami, and protected fetch wrapper
- Automatically refreshes access tokens when encountering 401 Unauthorized
- Computes authentication state and role-based capabilities

```mermaid
sequenceDiagram
participant V as "SignIn View"
participant S as "Auth Store"
participant EP as "Auth Endpoint"
V->>S : login({username,password})
S->>EP : POST /api/v1/auth/login
EP-->>S : {access_token, refresh_token, user}
S->>S : save tokens and expiry
S-->>V : success
Note over S : On protected request
S->>EP : GET /api/v1/auth/me (with Bearer)
EP-->>S : 401 Unauthorized
S->>EP : POST /api/v1/auth/refresh
EP-->>S : {access_token, refresh_token, user}
S->>EP : retry original request
EP-->>S : success
```

**Diagram sources**
- [frontend/src/stores/auth.js:29-177](file://frontend/src/stores/auth.js#L29-L177)
- [frontend/src/views/auth/SignIn.vue:25-38](file://frontend/src/views/auth/SignIn.vue#L25-L38)

**Section sources**
- [frontend/src/stores/auth.js:29-177](file://frontend/src/stores/auth.js#L29-L177)
- [frontend/src/views/auth/SignIn.vue:25-38](file://frontend/src/views/auth/SignIn.vue#L25-L38)

## Dependency Analysis
- Endpoints depend on services and schemas; services depend on models and security utilities; models depend on database base
- Security utilities depend on configuration for algorithm, secret key, and token durations
- Frontend depends on backend endpoints for authentication operations

```mermaid
graph LR
AUTH_EP["Auth Endpoints"] --> AUTH_SVC["Auth Service"]
AUTH_EP --> USER_SVC["User Service"]
AUTH_EP --> SEC_UTIL["Security Utilities"]
AUTH_SVC --> SEC_UTIL
AUTH_SVC --> USER_M["User Model"]
AUTH_SVC --> RT_M["RefreshToken Model"]
USER_SVC --> USER_M
SEC_UTIL --> CFG["Config"]
FE_STORE["Auth Store"] --> AUTH_EP
```

**Diagram sources**
- [backend/app/api/v1/endpoints/auth.py:1-106](file://backend/app/api/v1/endpoints/auth.py#L1-L106)
- [backend/app/services/auth_service.py:1-139](file://backend/app/services/auth_service.py#L1-L139)
- [backend/app/services/user_service.py:1-69](file://backend/app/services/user_service.py#L1-L69)
- [backend/app/core/security.py:1-99](file://backend/app/core/security.py#L1-L99)
- [backend/app/core/config.py:1-46](file://backend/app/core/config.py#L1-L46)
- [backend/app/models/user.py:1-35](file://backend/app/models/user.py#L1-L35)
- [backend/app/models/refresh_token.py:1-18](file://backend/app/models/refresh_token.py#L1-L18)
- [frontend/src/stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)

**Section sources**
- [backend/app/api/v1/endpoints/auth.py:1-106](file://backend/app/api/v1/endpoints/auth.py#L1-L106)
- [backend/app/services/auth_service.py:1-139](file://backend/app/services/auth_service.py#L1-L139)
- [backend/app/core/security.py:1-99](file://backend/app/core/security.py#L1-L99)
- [backend/app/core/config.py:1-46](file://backend/app/core/config.py#L1-L46)
- [frontend/src/stores/auth.js:1-198](file://frontend/src/stores/auth.js#L1-L198)

## Performance Considerations
- Token expiration windows: Access tokens are short-lived; refresh tokens are long-lived but tracked in the database for rotation and revocation
- Database queries: Token refresh requires a single lookup by JTI; revocation updates a single record; cleanup deletes expired records periodically
- Password hashing: bcrypt cost is implicit in salt generation; avoid excessive re-hashing during registration
- Frontend caching: Store tokens in secure storage and avoid unnecessary re-authentication by leveraging refresh automatically

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- Invalid or expired refresh token: Returned when JTI is missing, user not found, token revoked, or expired; client should log out and re-authenticate
- Disabled user: Login rejects inactive users; enable the account or contact an administrator
- Credentials validation failure: Incorrect username or password; ensure proper encoding and credentials
- 401 Unauthorized after initial login: Indicates access token expired; the frontend automatically attempts refresh; if refresh fails, prompt login again
- CORS errors: Verify allowed origins in configuration match the frontend origin

**Section sources**
- [backend/app/api/v1/endpoints/auth.py:26-36](file://backend/app/api/v1/endpoints/auth.py#L26-L36)
- [backend/app/api/v1/endpoints/auth.py:45-50](file://backend/app/api/v1/endpoints/auth.py#L45-L50)
- [backend/app/services/auth_service.py:45-74](file://backend/app/services/auth_service.py#L45-L74)
- [backend/app/core/security.py:61-79](file://backend/app/core/security.py#L61-L79)
- [frontend/src/stores/auth.js:168-177](file://frontend/src/stores/auth.js#L168-L177)

## Conclusion
The system implements a robust JWT-based authentication and authorization framework with refresh token rotation, role-based access control, and secure password handling. The backend provides clear separation of concerns across endpoints, services, models, and security utilities, while the frontend integrates seamlessly with the backend through a centralized authentication store. Adhering to the documented best practices and using the provided examples will ensure secure and maintainable authentication across the platform.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Endpoint Specifications and Schemas
- POST /api/v1/auth/login
  - Description: Authenticate user and return access and refresh tokens along with user info
  - Request: Form-encoded OAuth2 credentials (username, password)
  - Response: TokenPairWithUser
  - Errors: 401 Unauthorized (invalid credentials), 403 Forbidden (inactive user)

- POST /api/v1/auth/refresh
  - Description: Rotate access token using a valid refresh token
  - Request: RefreshRequest (refresh_token)
  - Response: TokenPairWithUser
  - Errors: 401 Unauthorized (invalid/expired refresh token)

- POST /api/v1/auth/register
  - Description: Register a new user (admin-only)
  - Request: UserCreate
  - Response: UserResponse
  - Errors: 400 Bad Request (duplicate username/email), 403 Forbidden (not admin)

- POST /api/v1/auth/logout
  - Description: Revoke the refresh token
  - Request: LogoutRequest (refresh_token)
  - Response: StatusResponse
  - Errors: None (best-effort revocation)

- GET /api/v1/auth/me
  - Description: Get current user info
  - Response: UserResponse
  - Errors: 401 Unauthorized, 403 Forbidden (inactive/admin checks)

- POST /api/v1/auth/init
  - Description: Initialize default admin if none exists
  - Response: StatusResponse

Schema references:
- TokenPairWithUser: [backend/app/schemas/auth.py:16-17](file://backend/app/schemas/auth.py#L16-L17)
- RefreshRequest: [backend/app/schemas/auth.py:20-21](file://backend/app/schemas/auth.py#L20-L21)
- LogoutRequest: [backend/app/schemas/auth.py:24-25](file://backend/app/schemas/auth.py#L24-L25)
- UserCreate/UserResponse: [backend/app/schemas/user.py:6-32](file://backend/app/schemas/user.py#L6-L32)
- StatusResponse: [backend/app/schemas/common.py:5-7](file://backend/app/schemas/common.py#L5-L7)

**Section sources**
- [backend/app/api/v1/endpoints/auth.py:20-105](file://backend/app/api/v1/endpoints/auth.py#L20-L105)
- [backend/app/schemas/auth.py:5-25](file://backend/app/schemas/auth.py#L5-L25)
- [backend/app/schemas/user.py:6-32](file://backend/app/schemas/user.py#L6-L32)
- [backend/app/schemas/common.py:5-7](file://backend/app/schemas/common.py#L5-L7)

### Security Best Practices
- Backend
  - Use HTTPS in production and configure CORS appropriately
  - Rotate refresh tokens on successful refresh and mark old ones revoked
  - Clean up expired refresh tokens regularly
  - Enforce role-based access checks for sensitive endpoints
  - Validate and sanitize all inputs; avoid exposing internal errors

- Frontend
  - Store tokens securely; avoid keeping long-lived tokens in memory
  - Implement automatic token refresh on 401 responses
  - Clear tokens on logout and redirect to login
  - Use HTTPS and secure cookies if applicable

[No sources needed since this section provides general guidance]