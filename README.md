# Books Review API

A FastAPI-based backend for managing books and their reviews, supporting CRUD operations, caching, and database migrations.

## Features

- **Books API**: Add, update, fetch, and delete books.
- **Reviews API**: Add, update, fetch, and delete reviews for books.
- **Database**: Uses SQLAlchemy ORM with PostgreSQL.
- **Caching**: Integrates Redis for caching book and review data.
- **Migrations**: Uses Alembic for database migrations.
- **CORS**: Configured for cross-origin requests.

## Project Structure

```
.
├── app/
│   ├── api/         # API routers for books and reviews
│   ├── core/        # Configuration and settings
│   ├── db/          # Database models, schemas, and session
│   ├── utils/       # Utility functions (cache, response, etc.)
│   └── main.py      # FastAPI entry point
├── alembic/         # Database migration scripts
├── requirements.txt # Python dependencies
└── alembic.ini      # Alembic configuration
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and set your database and Redis credentials.

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Books

- `POST /api/books/` — Add a new book
- `PATCH /api/books/` — Update book details
- `GET /api/books/` — Get all books or a specific book by `book_id`
- `DELETE /api/books/` — Delete a book by `book_id`

### Reviews

- `POST /api/reviews/` — Add a review to a book
- `PATCH /api/reviews/` — Update a review
- `GET /api/reviews/` — Get a review by `review_id`
- `DELETE /api/reviews/` — Delete a review by `review_id`

## Database Models

### Book

- `id`: Integer, primary key
- `book_name`: String
- `author`: String
- `description`: Text (optional)
- `language`: String
- `reviews`: Relationship to reviews

### Review

- `id`: Integer, primary key
- `book_id`: Foreign key to Book
- `reviewer_name`: String
- `ratings`: Integer
- `review`: Text

## Dependencies

- fastapi
- uvicorn
- pydantic-settings
- psycopg2-binary
- asyncpg
- alembic
- redis

## License

MIT 