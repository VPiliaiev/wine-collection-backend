
# wine-collection-backend
Wine Collection is a service that allows users to browse and purchase wines based on their taste preferences

## Environment variables
This project uses environment variables for configuration.

Copy `.env.sample` to `.env` and fill in required values.

## Environments
- dev: local development
- prod: cloud deployment (AWS/Azure)

## Tech stack
- Python 3.12
- Django Rest Framework
- PostgreSQL (prod)
- SQLite (dev, temporary)
- Docker & Docker Compose


## Installing using GitHub

Install PostgreSQL and create db

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

set POSTGRES_DB=<your_db_name>
set POSTGRES_USER=<your_db_user>
set POSTGRES_PASSWORD=<your_db_password>
set POSTGRES_HOST=<your_db_host>
set POSTGRES_PORT=<your_db_port>

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
python manage.py runserver
```

## Run with Docker

Docker should be installed.

```bash
docker-compose --build

docker-compose up
```

## Getting Access

Create user via "/api/user/register/".

Get access token "/api/user/token/".

## Features:

### Authentication
- JWT-authenticated API
- User registration and login

### Admin
- Admin panel accessible at `/admin/`
- Admin-only CRUD for:
  - Wines
  - Categories, moods, purposes, countries
  - Users

### Wines
- Public access: list and filter wines by:
  - Name
  - Mood
  - Category
  - Purpose
  - Country
  - Minimum & maximum price

### Cart
- Add/remove items to cart
- Automatic cart total calculation

### Documentation & Database
- Swagger API documentation available at `/api/doc/swagger/`
- PostgreSQL database integration
- Dockerized application