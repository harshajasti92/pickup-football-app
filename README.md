# Pickup Football App

A mobile-first web application for organizing pickup football games with smart team balancing.

## Project Structure

```
Pickup-Football/
├── database/              # PostgreSQL database schemas
│   └── 01_create_users_table.sql
├── backend/              # FastAPI backend application
│   ├── app/
│   │   └── main.py      # Main FastAPI application
│   ├── requirements.txt  # Python dependencies
│   ├── run.py           # Server startup script
│   └── README.md        # Backend documentation
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   └── signup/
│   │   │       ├── SignupForm.js
│   │   │       ├── SignupForm.css
│   │   │       └── index.js
│   │   └── App.js
│   └── package.json
└── README.md
```

## Features

### 🎯 Current Features (MVP)
- ✅ User registration form with validation
- ✅ FastAPI backend with PostgreSQL integration
- ✅ Password hashing and security
- ✅ Real-time form validation
- ✅ Full-stack connectivity (React ↔ FastAPI ↔ PostgreSQL)
- ✅ Responsive design optimized for mobile

### 🚀 Planned Features
- User authentication and login
- Game creation and management
- Smart team balancing algorithm
- Player statistics dashboard
- Mobile-optimized interface

## Database Schema

The `users` table includes:
- Basic info (username, password, name, phone)
- Age range constraints ('18-25', '26-35', '36-45', '46+')
- Skill level (1-10 scale)
- Position preferences (Goalkeeper, Defender, Midfielder, Forward, Any)
- Playing styles (Aggressive, Technical, Physical, Balanced, Creative, Defensive)
- Account management (verification, active status)
- Timestamps with auto-update triggers

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- PostgreSQL (v17)
- npm or yarn

### Database Setup
1. Ensure PostgreSQL is running locally
2. Execute the database schema:
   ```bash
   psql -U postgres -f database/01_create_users_table.sql
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python run.py
   ```

4. API will be available at http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/health/db

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open http://localhost:3000 in your browser


## Quick Start

### 🚀 Run the Application
```bash
# 1. Start Backend (Terminal 1)
cd backend
python run.py
# Server starts at http://localhost:8000

# 2. Start Frontend (Terminal 2)  
cd frontend
npm start
# App opens at http://localhost:3000
```

### ✅ Test Signup Functionality
1. Open http://localhost:3000
2. Fill out the signup form
3. Check database with: `cd backend && python check_users.py`

## Development

### Frontend Technologies
- React 18
- CSS3 with responsive design
- Form validation and error handling
- Modern ES6+ JavaScript
- API integration with fetch

### Backend Technologies
- FastAPI (Python)
- PostgreSQL integration with psycopg2
- Bcrypt password hashing
- Pydantic data validation
- Uvicorn ASGI server
- CORS middleware for frontend integration

### Database Technologies
- PostgreSQL 17
- SQL constraints for data integrity
- Indexing for performance
- Triggers for automatic timestamps

## API Integration (✅ Complete!)

The signup form now connects to a FastAPI backend that:
1. ✅ Validates user input using Pydantic models
2. ✅ Hashes passwords securely with bcrypt
3. ✅ Stores user data in PostgreSQL database
4. ✅ Returns success/error responses to frontend
5. ✅ Provides API documentation at `/docs`

## Running the Full Stack

1. **Start PostgreSQL** (ensure it's running)
2. **Start Backend API**:
   ```bash
   cd backend && python run.py
   ```
3. **Start Frontend**:
   ```bash
   cd frontend && npm start
   ```

Then visit http://localhost:3000 to use the app!

## Mobile Optimization

The interface is designed mobile-first with:
- Responsive breakpoints for all screen sizes
- Touch-friendly form controls
- Optimized typography and spacing
- Progressive web app capabilities (planned)

## Contributing

This is currently a personal project for learning full-stack development. Future contributions welcome!

## License

MIT License - feel free to learn from this code!
