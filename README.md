# Scrible

A RESTful social media API built with **FastAPI** and **PostgreSQL**, featuring JWT authentication, post management, and a voting system.

## Features

- **User accounts** — registration with hashed passwords
- **JWT authentication** — login returns a bearer token for protected routes
- **Posts** — create, read, update, and delete, with pagination and search
- **Voting** — upvote/remove-vote on posts, with vote counts returned alongside posts
- **Ownership checks** — only a post's owner can update or delete it
- **Auto-generated docs** — interactive Swagger UI and ReDoc
- **Database migrations** — schema versioning via Alembic
- **Dockerized** — one command to spin up the API and database together

## Tech Stack

| Layer      | Technology              |
| ---------- | ----------------------- |
| Language   | Python 3.11             |
| Framework  | FastAPI                 |
| Database   | PostgreSQL 16           |
| ORM        | SQLAlchemy              |
| Migrations | Alembic                 |
| Auth       | JWT (PyJWT)             |
| Testing    | pytest                  |
| Containers | Docker / Docker Compose |

## Getting Started

### Prerequisites

- **Docker:** Docker & Docker Compose
- **Local:** Python 3.10+, PostgreSQL 16+, pip

### Environment Variables

Create a `.env` file in the project root:

```env
DB_HOSTNAME=localhost   # use "db" when running with Docker Compose
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_NAME=social_media_db

SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run with Docker (recommended)

```bash
git clone https://github.com/Yusuph-Darbo/Scrible.git
cd Scrible
# create .env with DB_HOSTNAME=db
docker compose -f docker-compose-dev.yml up --build
docker compose -f docker-compose-dev.yml exec api alembic upgrade head
```

The API is now available at `http://localhost:8000`.

### Run Locally

```bash
git clone https://github.com/Yusuph-Darbo/Scrible.git
cd Scrible
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# create .env with DB_HOSTNAME=localhost, then create the database
alembic upgrade head
uvicorn app.main:app --reload
```

### Migrations

```bash
alembic upgrade head                        # apply latest migrations
alembic revision --autogenerate -m "message"  # generate a new migration
alembic downgrade -1                          # roll back one migration
```

## Authentication

1. Register via `POST /users/`
2. Log in via `POST /login` with form data (`username` = email, `password`)
3. Send the returned token on protected routes: `Authorization: Bearer <token>`

### Interactive Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Use the **Authorize** button in Swagger UI to test protected routes with your token.

## Running Tests

Tests use `pytest` and expect a separate `<DB_NAME>_test` PostgreSQL database (created automatically per run, using the same credentials as `.env`).

```bash
pytest
```
