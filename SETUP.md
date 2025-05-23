# OneTouch App Setup Instructions

## Overview
This guide provides instructions for setting up the OneTouch application using either Docker (recommended) or manual installation.

## Option 1: Using Docker (Recommended)

### Prerequisites
1. Install Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop)
2. Install Docker Compose (usually comes with Docker Desktop)

### Steps to Run with Docker

1. **Clone the Repository**
```bash
git clone <repository-url>
cd onetouch-app
```

2. **Configure Environment**
Create a `docker-compose.override.yml` file in the root directory with the following content:
```yaml
services:
  backend:
    environment:
      - ADMIN_USERNAME=secret_admin
      - ADMIN_PASSWORD=secret_password
      - DATABASE_URL=sqlite:///onetouch.db
      - SECRET_KEY_FOR_TOKEN=secret_key
      - ALGORITHM_FOR_TOKEN=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Build and Run**
```bash
docker-compose up --build
```

## Option 2: Manual Setup (Without Docker)

### Prerequisites
1. Python 3.11 or higher
2. pip (Python package manager)
3. Git

### Steps to Run Manually

1. **Clone the Repository**
```bash
git clone <repository-url>
cd onetouch-app
```

2. **Create and Activate Virtual Environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
Create a `.env` file in the root directory with the following content:
```env
DATABASE_URL=sqlite:///onetouch.db
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=your_secure_password
SECRET_KEY_FOR_TOKEN=your_secret_key_here
ALGORITHM_FOR_TOKEN=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run the Application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

## Verifying the Setup

### 1. Check API Health
Visit `http://localhost:8002` in your browser or use curl:
```bash
curl http://localhost:8002
```
Expected response: `{"message": "Hello World from OneTouch backend"}`

### 2. Access API Documentation
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

### 3. Test Authentication
1. Use the `/api/token` endpoint to get an access token
2. Use the admin credentials you set in the environment configuration
3. Include the token in subsequent requests using the Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```

## Troubleshooting

### Common Issues
1. **Port Already in Use**
   - Ensure no other service is running on port 8002
   - Change the port in the run command if needed

2. **Database Connection Issues**
   - Verify the DATABASE_URL in your environment configuration
   - Ensure the database directory is writable

3. **Authentication Problems**
   - Double-check your ADMIN_USERNAME and ADMIN_PASSWORD
   - Verify the SECRET_KEY_FOR_TOKEN is properly set




