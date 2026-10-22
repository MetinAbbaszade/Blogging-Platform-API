# Blogging Platform API

A RESTful API for a personal blogging platform. It supports basic CRUD operations on blog posts. Built as a solution to the [roadmap.sh Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api) project.

## Tech Stack

- **Python** 3.12+
- **FastAPI**: web framework
- **SQLModel / SQLAlchemy**: ORM
- **MySQL** via **PyMySQL**: database
- **Uvicorn**: ASGI server
- **Poetry**: dependency management

## Project Structure

```
.
├── run.py                        # Entry point: creates tables and starts the server
├── app/
│   ├── __init__.py               # App factory, DB engine, table creation
│   ├── extensions.py             # DB session dependency (get_db)
│   ├── api/v1/
│   │   ├── endpoints/posts.py    # Post routes
│   │   └── schema/posts.py       # Pydantic request/response schemas
│   ├── models/
│   │   ├── basemodel.py          # Base model (id, timestamps)
│   │   └── post.py               # Post table model
│   ├── persistence/
│   │   └── repository.py         # Repository interface and implementation
│   └── service/
│       └── facade.py             # Service layer between routes and repository
├── pyproject.toml
└── poetry.lock
```

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)
- A running MySQL server

### Installation

```bash
git clone https://github.com/MetinAbbaszade/Blogging-Platform-API.git
cd Blogging-Platform-API
poetry install
```

### Database Setup

Create the database in MySQL:

```sql
CREATE DATABASE Post_Database;
```

Then set your connection string in `app/__init__.py`:

```python
URL = 'mysql+pymysql://<user>:<password>@localhost/Post_Database'
```

The tables are created automatically when the app starts.

### Running the Server

```bash
poetry run python run.py
```

The API runs at `http://localhost:8000`. Interactive docs are available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

Base path: `/api/v1/post`

| Method   | Endpoint              | Description         | Success Code |
|----------|-----------------------|---------------------|--------------|
| `GET`    | `/api/v1/post/`       | Get all posts       | `200`        |
| `GET`    | `/api/v1/post/{id}`   | Get a post by ID    | `200`        |
| `POST`   | `/api/v1/post/`       | Create a new post   | `201`        |
| `PUT`    | `/api/v1/post/{id}`   | Update a post       | `200`        |
| `DELETE` | `/api/v1/post/{id}`   | Delete a post       | `204`        |

If the post (or, for `GET /`, any post) is not found, the API returns `404`.

### Create a Post

```http
POST /api/v1/post/
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

Response `201 Created`:

```json
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

### Get a Post

```http
GET /api/v1/post/{id}
```

Response `200 OK`:

```json
{
  "id": "1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed",
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "created_by": "2025-01-01T12:00:00",
  "updated_by": "2025-01-01T12:00:00"
}
```

### Update a Post

```http
PUT /api/v1/post/{id}
Content-Type: application/json

{
  "title": "My Updated Blog Post",
  "content": "This is the updated content.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

Response `200 OK` with the updated post.

### Delete a Post

```http
DELETE /api/v1/post/{id}
```

Response `204 No Content`.

## Post Fields

| Field        | Type       | Description                            |
|--------------|------------|----------------------------------------|
| `id`         | `string`   | UUID, generated automatically          |
| `title`      | `string`   | Post title (max 100 characters)        |
| `content`    | `string`   | Post body                              |
| `category`   | `string`   | Post category                          |
| `tags`       | `string[]` | List of tags                           |
| `created_by` | `datetime` | Creation timestamp, set automatically  |
| `updated_by` | `datetime` | Last update timestamp, set automatically |
