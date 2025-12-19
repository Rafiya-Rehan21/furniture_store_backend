# Furniture Store Backend

This is a **Django + Django REST Framework (DRF)** backend for a furniture e-commerce store.
It is **dockerized** and uses **PostgreSQL 17** for development.

## Features

* User authentication (JWT-based login/registration) 
* Product, Category, Order, and Cart management
* REST API endpoints for frontend consumption
* Dockerized development environment

## Tech Stack

* Python 3.11
* Django 5.2
* Django REST Framework 3.16
* PostgreSQL 17 (via Docker)
* Docker + Docker Compose

## Setup (Development)

1. **Clone the repository:**

```bash
git clone <repo-url>
cd furniture_store_backend
```

2. **Copy `.env.example` to `.env`** (if you have environment variables)

3. **Build and start Docker containers:**

```bash
docker-compose up --build
```

4. **Apply migrations:**

```bash
docker-compose exec web python manage.py migrate
```

5. **Create a superuser (optional, for admin access):**

```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Access the development server:**

```
http://localhost:8000/
```

---

## Notes

* Use `feature/<feature-name>` branches for new features
* PRs should be **Rebase and Merge** into `dev`
* Keep `dev` branch up to date before starting new features
