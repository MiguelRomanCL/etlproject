# MSW KPI Conversion

A FastAPI application for calculating conversion KPIs for livestock management (M1 project).

**Autor:** Cristobal Balladares

## Description

This project provides an API service for calculating conversion metrics based on animal breeding, weight, food consumption, and mortality data. It's designed to work with PostgreSQL and Redis for data storage and caching.

## Features

- RESTful API for conversion calculations
- PostgreSQL database integration
- Redis caching support
- Data processing with Polars
- SQLModel for database operations

## Requirements

- Python >= 3.12
- PostgreSQL database
- Redis server
- UV package manager (recommended) or pip

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd msw-kpi-conversion
```

### 2. Set up environment variables

Create a `.env` file in the root directory with the following variables:

```env
POSTGRES_SERVER=your_postgres_host
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DATABASE=your_postgres_database
PROJECT_NAME=MSW-KPI-Conversion
```

### 3. Install dependencies

Using UV (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

For development dependencies:

```bash
uv sync --dev
```

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
cd src
python main.py
```

The API will be available at `http://localhost:8000`

### Production Mode

Using uvicorn directly:

```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access:

- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### POST /conversion

Calculate conversion metrics based on breeding, weight, food consumption, and mortality data.

**Request:**
- Method: POST
- URL: `/conversion`
- Body: None (uses database session)

**Response:**
- Status: 200 OK
- Body: List of conversion calculation results

**Example:**

```bash
curl -X POST http://localhost:8000/conversion
```

## Project Structure

```
msw-kpi-conversion/
├── src/
│   ├── main.py                     # Application entry point
│   ├── app/
│   │   ├── config/                 # Configuration files
│   │   │   ├── config.py           # Environment variables
│   │   │   └── logger.py           # Logging configuration
│   │   ├── db/                     # Database connections
│   │   │   ├── sql/                # PostgreSQL setup
│   │   │   └── redis/              # Redis setup
│   │   ├── models/                 # Database models
│   │   │   ├── animal_weights.py
│   │   │   ├── breedings.py
│   │   │   ├── conversion.py
│   │   │   ├── entities.py
│   │   │   ├── food_consumptions.py
│   │   │   └── mortality.py
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── conversion.py
│   │   │   └── polars.py
│   │   ├── routers/                # API routes
│   │   │   └── conversion.py
│   │   ├── services/               # Business logic
│   │   │   └── conversion.py
│   │   └── utilities/              # Helper functions
│   │       ├── get_data.py
│   │       └── timers.py
├── pyproject.toml                  # Project dependencies
├── .env                            # Environment variables
└── README.md                       # This file
```

## Development

### Code Quality Tools

This project uses several code quality tools configured in `pyproject.toml`:

- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **Ruff**: Fast Python linter
- **autoflake**: Remove unused imports and variables
- **pre-commit**: Git hooks for code quality

### Install pre-commit hooks

```bash
pre-commit install
```

### Run pre-commit manually

```bash
pre-commit run --all-files
```

## Dependencies

### Core Dependencies
- FastAPI >= 0.119.0 - Web framework
- Uvicorn >= 0.37.0 - ASGI server
- SQLAlchemy >= 2.0.44 - SQL toolkit
- SQLModel >= 0.0.27 - SQL databases with Python objects
- Polars >= 1.34.0 - Fast DataFrame library
- psycopg2-binary >= 2.9.11 - PostgreSQL adapter
- Redis >= 6.4.0 - Redis client

### Development Dependencies
- pre-commit >= 4.3.0 - Git hook scripts

## Version

Current version: 0.1.0
