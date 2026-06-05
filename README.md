# Social Media API

A RESTful API built with **FastAPI** and **PostgreSQL** for user registration, JWT authentication, post management, and voting.

**Stack:** Python 3.11 · FastAPI · PostgreSQL 16 · SQLAlchemy · Alembic · JWT · Docker

## Setup

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

### Docker (recommended)

```bash
git clone https://github.com/Yusuph-Darbo/social_media_api.git
cd social_media_api
# create .env with DB_HOSTNAME=db
docker compose -f docker-compose-dev.yml up --build
docker compose -f docker-compose-dev.yml exec api alembic upgrade head
```

API runs at `http://localhost:8000`.

### Local

```bash
git clone https://github.com/Yusuph-Darbo/social_media_api.git
cd social_media_api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# create .env with DB_HOSTNAME=localhost, then create the database
alembic upgrade head
uvicorn app.main:app --reload
```

**Migrations:** `alembic upgrade head` · `alembic revision --autogenerate -m "message"` · `alembic downgrade -1`

## Authentication

1. Register via `POST /users/`
2. Log in via `POST /login` with form data (`username` = email, `password`)
3. Send the returned token on protected routes: `Authorization: Bearer <token>`

## API Routes

| Method   | Path          | Auth | Description                                                           |
| -------- | ------------- | :--: | --------------------------------------------------------------------- |
| `GET`    | `/`           |      | Health check                                                          |
| `POST`   | `/users/`     |      | Register user — body: `{ email, password }`                           |
| `GET`    | `/users/{id}` |      | Get user by ID                                                        |
| `POST`   | `/login`      |      | Login — form fields: `username`, `password` → `{ token, token_type }` |
| `GET`    | `/posts/`     |  ✓   | List posts — query: `limit`, `skip`, `search`                         |
| `POST`   | `/posts/`     |  ✓   | Create post — body: `{ title, content, published? }`                  |
| `GET`    | `/posts/{id}` |  ✓   | Get post with vote count                                              |
| `PUT`    | `/posts/{id}` |  ✓   | Update post (owner only)                                              |
| `DELETE` | `/posts/{id}` |  ✓   | Delete post (owner only)                                              |
| `POST`   | `/vote/`      |  ✓   | Vote — body: `{ post_id, dir }` (`1` = upvote, `0` = remove)          |

List/get post responses include `{ post, votes }`. Post updates and deletes return `403` if the caller is not the owner.

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Use the **Authorize** button in Swagger UI to test protected routes.

## Quick Example

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'

curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword"

curl http://localhost:8000/posts/ -H "Authorization: Bearer <token>"
```
