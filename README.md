# dzeencode-test-task


This project is a Django-based RESTful API for managing comments. The API allows users to create and view comments.

## Features

- **Comment creation**:
  - add files and use html tags
- **User Registration and Authentication**:
  - Secure user registration and login.
  - Token-based authentication using JSON Web Tokens (JWT).
- **Advanced Features**:
  - Sort comments by username, creation date or email
- **Dockerized**:
  - Simplified deployment using Docker.
- **API Documentation**:
  - Integrated Swagger documentation.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (for containerized setup)
- PostgreSQL

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/SysoevDmitro/dzeencode-test-task.git
   cd dzeencode-test-task
   ```
2. **Create a Virtual Environment:**
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Apply Migrations:**
   ```
   python manage.py makemigrations
   ```
5. **Create .env file with your parameters from .env_sample:**
   ```
    SECRET_KEY=
    POSTGRES_PASSWORD=
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_HOST=
    POSTGRES_PORT=

   ```

6. **Run with Docker:**
   ```
   docker-compose up --build
   ```

### Documentation
- Go to `/api/doc/swagger/` to test api
  - Register with `/user/register/`
  - Receive token `/user/token/`
  - Create comment `/api/comments/`
