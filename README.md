# 📋 Task Manager – FastAPI + Frontend

A full-stack task management application built with **FastAPI** (Python) and a **vanilla HTML/CSS/JS** frontend.

## ✨ Features

- **User Authentication** – Register, login with JWT-based auth & bcrypt password hashing
- **Task Management** – Create, read, update, delete tasks
- **Task Filtering** – Filter by completion status (`?completed=true/false`)
- **Pagination** – Paginated task listing (`?skip=0&limit=10`)
- **Ownership Isolation** – Each user can only access their own tasks
- **Interactive API Docs** – Swagger UI at `/docs`

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | SQLite (local) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest, httpx |

## 📂 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models.py         # User & Task ORM models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── auth.py           # JWT & password utilities
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

## 🚀 Setup & Run Locally

### 1. Clone the repository

```bash
git clone git@github.com:YOUR_USERNAME/task-manager-fastapi.git
cd task-manager-fastapi
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
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

## 🧪 Run Tests

```bash
cd backend
pytest tests/ -v
```

## 🌐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing secret | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | Database connection string | `sqlite:///./tasks.db` |

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | ❌ | Register new user |
| POST | `/login` | ❌ | Login & get JWT token |
| POST | `/tasks/` | ✅ | Create a task |
| GET | `/tasks/` | ✅ | List tasks (pagination + filter) |
| GET | `/tasks/{id}` | ✅ | Get a specific task |
| PUT | `/tasks/{id}` | ✅ | Update a task |
| DELETE | `/tasks/{id}` | ✅ | Delete a task |

## 🐳 Docker

```bash
docker build -t task-manager .
docker run -p 8000:8000 task-manager
```

## 🔗 Deployment

- **Live URL**: _[To be added after deployment]_
- **API Docs**: _[Live URL]/docs_
