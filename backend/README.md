# Pickup Football Backend API

FastAPI backend for the Pickup Football application.

## Features

- ✅ User registration with password hashing
- ✅ PostgreSQL database integration
- ✅ Data validation using Pydantic
- ✅ CORS support for React frontend
- ✅ Health check endpoints
- ✅ Auto-reload for development

## API Endpoints

### Health & Status
- `GET /` - API health check
- `GET /api/health/db` - Database connection check

### User Management
- `POST /api/users/signup` - Create new user account
- `GET /api/users/{user_id}` - Get user by ID

## Running the API

1. Make sure PostgreSQL is running and the users table is created
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Connection

The API connects to PostgreSQL using these default settings:
- Host: localhost
- Database: postgres
- User: postgres
- Password: postgres (or set POSTGRES_PASSWORD environment variable)

## Security Features

- Passwords are hashed using bcrypt
- Input validation using Pydantic models
- SQL injection protection with parameterized queries
- CORS configured for frontend integration
