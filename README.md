# Task Manager - FastAPI + Frontend

A full-stack task management application built with **FastAPI** (Python) and a **vanilla HTML/CSS/JS** frontend.

## Features

- **User Authentication** - Register, login with JWT-based auth and bcrypt password hashing
- **Task Management** - Create, read, update, delete tasks
- **Task Filtering** - Filter by completion status (`?completed=true/false`)
- **Pagination** - Paginated task listing (`?skip=0&limit=10`)
- **Ownership Isolation** - Each user can only access their own tasks
- **Interactive API Docs** - Swagger UI at `/docs`

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | SQLite (local), PostgreSQL (production) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest, httpx |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models.py         # User and Task ORM models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── auth.py           # JWT and password utilities
│   │   ├── dependencies.py   # Auth dependency
│   │   └── routers/
│   │       ├── auth.py       # /register, /login
│   │       └── tasks.py      # /tasks CRUD
│   ├── tests/
│   │   ├── conftest.py       # Test fixtures
│   │   ├── test_auth.py      # Auth tests
│   │   └── test_tasks.py     # Task tests
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── Dockerfile
├── .gitignore
└── README.md
```

## Setup and Run Locally

### 1. Clone the repository

```bash
git clone git@github.com:Sasivisvan/task-manager-fastapi.git
cd task-manager-fastapi
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Set environment variables

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and set a secure SECRET_KEY
```

### 5. Run the server

```bash
cd backend
uvicorn app.main:app --reload
```

### 6. Open in browser

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Run Tests

```bash
cd backend
pytest tests/ -v
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing secret | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | Database connection string | `sqlite:///./tasks.db` |

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Register new user |
| POST | `/login` | No | Login and get JWT token |
| POST | `/tasks/` | Yes | Create a task |
| GET | `/tasks/` | Yes | List tasks (pagination + filter) |
| GET | `/tasks/{id}` | Yes | Get a specific task |
| PUT | `/tasks/{id}` | Yes | Update a task |
| DELETE | `/tasks/{id}` | Yes | Delete a task |

## Docker

```bash
docker build -t task-manager .
docker run -p 8000:8000 task-manager
```

## Deployment

- **Live URL**: https://task-manager-fastapi-ne1e.onrender.com
- **API Docs**: https://task-manager-fastapi-ne1e.onrender.com/docs
