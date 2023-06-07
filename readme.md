# **Project Name**

This is a project using Python, FastAPI, and MySQL.

### **Installation**

To run the project using Docker, make sure you have installed **docker** and **docker-compose**, then follow these steps:

1. Clone this repository: 
``` bash
git clone https://github.com/codechrl/challenge-library.git
```

2. Navigate to directory
``` bash
cd challenge-library
```

3. Build & Run the Docker image: 
``` bash
docker-compose up --build
```

The above command will run the project inside a Docker container and expose it on port 8000.

## **Usage**

Once the app is running, you can access the Swagger UI API at **`http://localhost:8000/api/docs`**.

Also you can access the OpenAPI Redoc at **`http://localhost:8000/api/redoc`**.
