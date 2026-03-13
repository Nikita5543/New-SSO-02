# NOC Vision - Network Operations Center Platform

A modern, plugin-based Network Operations Center (NOC) platform built with FastAPI backend and Vue 3 frontend.

## Project Structure

```
NOC Vision/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configuration, security, database
│   │   ├── models/      # SQLAlchemy database models
│   │   ├── plugins/     # Plugin system (6 built-in plugins)
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic services
│   ├── requirements.txt
│   └── run.py
├── frontend/            # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── layouts/     # Layout components
│   │   ├── plugins/     # Plugin frontend views
│   │   ├── router/      # Vue Router configuration
│   │   ├── stores/      # Pinia state management
│   │   └── views/       # Page views
│   ├── package.json
│   └── index.html
├── docker-compose.yml   # Docker orchestration
└── .env.example         # Environment variables template
```

## Features

### Core System
- 🔐 **Authentication & Authorization** - JWT-based auth with refresh tokens
- 👥 **User Management** - Role-based access control (admin/user)
- 🔌 **Plugin Architecture** - Dynamic plugin loading system
- 🎨 **Modern UI** - Beautiful, responsive interface with dark mode support

### Built-in Plugins

1. **Incidents** - Network incident management and tracking
2. **Inventory** - Network equipment and asset management
3. **Performance** - Performance monitoring and metrics
4. **Security Module** - Security event monitoring
5. **Accounting** - Resource accounting and billing
6. **Configuration** - Network device configuration management

### Frontend Features
- Component library based on shadcn/ui
- Responsive dashboard layout
- Plugin registry with dynamic menu generation
- Real-time authentication state management
- Tailwind CSS styling

## Prerequisites

You need the following software installed:

1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **PostgreSQL 16+** - [Download](https://www.postgresql.org/download/) OR use Docker

## Quick Start Guide

### Option 1: Using Docker (Recommended)

If you have Docker installed:

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

Default admin credentials:
- Username: `admin`
- Password: `admin`

### Option 2: Manual Setup

#### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example .env

# Run database migrations (if using Alembic)
alembic upgrade head

# Start the backend server
python run.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### Step 2: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file if needed
# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173` or `http://localhost:3000`

## Configuration

Edit the `.env` file to configure your environment:

```env
# Database
DATABASE_URL=postgresql+psycopg2://noc:noc_password@localhost:5432/noc_vision

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Application
DEBUG=true
LOG_LEVEL=INFO

# Plugins (empty = all enabled)
ENABLED_PLUGINS=

# Default admin
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin
DEFAULT_ADMIN_EMAIL=admin@nocvision.local
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Adding a New Plugin

1. Create plugin directory in `backend/app/plugins/your_plugin/`
2. Implement required files:
   - `plugin.py` - Plugin metadata and registration
   - `models.py` - Database models
   - `schemas.py` - Pydantic schemas
   - `endpoints.py` - API routes
3. Create frontend views in `frontend/src/plugins/your_plugin/views/`
4. Add menu items in `frontend/src/main.js`

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python run.py  # Auto-reload enabled
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev  # Hot reload enabled
```

## Database

The application uses PostgreSQL with SQLAlchemy ORM. Tables are automatically created on startup for development. For production, use Alembic migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check if PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Frontend won't start:**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if backend is running at http://localhost:8000
- Verify CORS settings in .env match your frontend URL

**Database connection errors:**
- Ensure PostgreSQL service is running
- Check database credentials in DATABASE_URL
- Create database if it doesn't exist: `createdb -U noc noc_vision`

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- JWT - Authentication
- Alembic - Database migrations

**Frontend:**
- Vue 3 - Progressive JavaScript framework
- Vite - Next generation frontend tooling
- Pinia - State management
- Vue Router - Routing
- Tailwind CSS - Utility-first CSS
- Lucide Icons - Beautiful icons

**Infrastructure:**
- PostgreSQL - Database
- Docker & Docker Compose - Containerization
- Nginx - Reverse proxy (in production)

## License

MIT License

## Support

For issues and questions, please open an issue on the project repository.

---

Built with ❤️ by NOC Vision Team
