# 🗨️ Commentate

**Commentate** is a small FastAPI-based backend game designed to manage friends' comments with filtering and categorization. Built with **FastAPI**, **PostgreSQL**, and **Docker**, it supports robust API endpoints to add, retrieve, and filter comments.

---

## 🚀 Features

- **FastAPI Framework**: High-performance, modern Python API.
- **PostgreSQL Database**: Manages comment data with structured categories.
- **Dynamic Filtering**: Query comments by name or category.
- **Dockerized**: Fully containerized for easy deployment and local development.
- **Pydantic Validation**: Ensures clean and structured API input/output.
- **Testing**: Comprehensive tests using `pytest` and `pytest-asyncio`.

---
## ⚙️ Prerequisites

Ensure you have the following installed:
- [Python 3.10+](https://www.python.org/)
- [Docker](https://www.docker.com/get-started)
- [PostgreSQL](https://www.postgresql.org/)
- [Git](https://git-scm.com/)

---

## 🔧 Setup Instructions

1. **Clone the Repository**:
    ```
    git clone https://github.com/andrewbeshay25/commentate.git
    cd commentate
    ```
2. **Setup Environment Variables**: Create a .env file in the root directory with the following:

    ```
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=yourpassword <-- replace with your own password
    DATABASE_NAME=Commentate
    DATABASE_HOST=db
    DATABASE_PORT=5432
    ```
3. **Build and Run Using Docker**:
    ```
    docker-compose up --build
    ```
4. **Access the Application**:
- API Documentation: http://localhost:8000/docs
- Interactive Swagger UI to test endpoints.

## 🚀 Usage
### API Endpoints

1. **Fetch All Comments**:
    ```
    GET /comments/
    ```
2. **Filter Comments**: Query parameters:
    - ```name```: Filter by comment name.
    - ```category```: Filter by comment category.
Example:
    ```
    GET /comments/?name=John&category=compliment
    ```
3. **Add a Comment**:
    ```
    POST /comments/
    ```
4. **Request Body**:
    ```
    {
      "message": "You are amazing!",
      "name": "Alice",
      "category": "compliment"
    }
    ```

## 🧪 Testing
1. **Run Tests Locally**:
    ```
    pytest --asyncio-mode=auto
    ```
2. **GitHub Actions CI**: The test.yml GitHub Actions workflow ensures that the code is tested automatically on every push.


## 🐳 Docker

- Build and run the containers with Docker Compose:
    ```
    docker-compose up --build
    ```
- Stop your container:
    ```
    docker-compose down
    ```
## 🔒 Security
- Sensitive credentials (e.g., database passwords) are managed using environment variables (.env file).

## 🎉 Author
Developed with ❤️ by Andrew Beshay.
