# INFORCE Python Task — Lunch Voting Service

## Overview

This project implements a backend service that helps employees decide where to have lunch.  
Restaurants upload their menus daily through an API, and employees vote for their preferred menu before going to lunch.

The backend supports multiple versions of the mobile app by reading the **`Build-Version`** header from requests, allowing older clients to receive legacy responses while newer clients use the updated API.

---

## Features

- **Authentication** using JWT (login, register, token refresh)
- **Restaurant Management**: Create restaurants, upload daily menus
- **Menu Management**: Get current day's menu
- **Voting System**: Employees vote for a menu once per day
- **Results**: Retrieve current day's voting results
- **API Versioning Support** via request headers (`Build-Version`)

---

## Tech Stack

- **Python 3**
- **Django** + **Django REST Framework**
- **PostgreSQL**
- **JWT Authentication** (via `djangorestframework-simplejwt`)
- **Docker** + **docker-compose**
- **Pytest** for testing
- **flake8** for code style checking

---

## API Endpoints

### Auth

- `POST /api/auth/register/` — Create new user
- `POST /api/auth/login/` — Obtain JWT tokens
- `POST /api/auth/token/refresh/` — Refresh access token

### Restaurants

- `POST /api/restaurants/` — Create a restaurant (authenticated)
- `POST /api/restaurants/{id}/menu/` — Add daily menu for a restaurant (authenticated)
- `GET /api/restaurants/menu/today/` — Get today's menu

### Votes

- `POST /api/votes/` — Vote for a menu (authenticated, only once per day)
- `GET /api/votes/results/today/` — Get today's voting results

---

## Running Locally (Manual Setup)

### Prerequisites

- Python 3.10+
- PostgreSQL
- Virtualenv (recommended)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/UgrynBohdan/INFORCE-Python-Task.git
   cd INFORCE-Python-Task
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## Running with Docker Compose

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Copy docker-compose.yml and .env files from GitHub**

2. **Start containers**

   ```bash
   docker-compose up
   ```

3. **Access the application**

   ```
   http://localhost:8000
   ```

---

## Running Tests

```bash
pytest
```

---

## Code Quality

To check code style:

```bash
flake8 .
```

---

## Notes

- Make sure PostgreSQL service is running and accessible when running locally.
- JWT authentication is required for creating restaurants, menus, and voting.
- The API automatically adapts responses depending on the `Build-Version` header in requests.
