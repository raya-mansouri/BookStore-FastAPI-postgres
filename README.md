# BookStore-FastAPI-Postgres

A Bookstore API built with FastAPI and PostgreSQL, providing endpoints to manage books and authors.

## Features

- **CRUD Operations**: Create, read, update, and delete books and authors.
- **Database Integration**: Utilizes PostgreSQL for data storage.
- **API Documentation**: Interactive API docs available via Swagger UI.

## Prerequisites

- **Python 3.10+**
- **PostgreSQL**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/raya-mansouri/BookStore-FastAPI-postgres.git
cd BookStore-FastAPI-postgres
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
```

Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your PostgreSQL credentials and database details.

### 5. Apply Database Migrations

```bash
alembic upgrade head
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`. Access the interactive API documentation at `http://127.0.0.1:8000/docs`.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.


