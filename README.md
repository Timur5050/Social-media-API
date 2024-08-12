# Social-media-API

This Social Media API, built using Django Rest Framework (DRF), leverages RESTful architecture to provide robust and efficient access to social media functionalities. It allows seamless integration and interaction with social media features such as user authentication, post creation, comment management, and more, facilitating a smooth and scalable user experience.

# Features
- Celery
- Redis
- JWT authentication
- Admin panel
- Comfortable documentation
- Managing profile
- Creating posts, likes and comments
- Schedule posts creation with celery
- Docker and docker-compose
- PostgreSQL
- Permissions
- Swagger documentation

# Run program using GitHub
To run Celery with both a worker in separate terminals, you can follow these instructions. This will ensure your Celery tasks are processed and scheduled correctly. Below is a step-by-step guide for setting up and starting the Celery worker.

### You need to have docker installed
```sh
# Clone the repository
git clone https://github.com/Timur5050/social_media_api.git
# Change to the project directory
cd social_media_api
# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install required packages
pip install -r requirements.txt
# Create new Postgres DB & User
# Copy sample.env -> .env and populate with all required data 
# Apply migrations
python manage.py migrate

# Run Redis Server
docker run -d -p 6379:6379 redis

# Terminal 2: Start Celery Worker
- celery -A social_media_api worker --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo

# Create schedule for running sync in DB
run app: python manage.py runserver
```

# Run with docker
### You need to have docker
```sh
# Clone the repository
git clone https://github.com/Timur5050/social_media_api.git
# Change to the project directory
cd social_media_api
# Copy sample.env -> .env and populate with all required data 
# Build and run docker-compose
docker-compose up --build
```

# Getting access
- create user via /api/user/register/
- get access token via api/user/login/

# Full documentation
Get in Browser:
<br>
http://127.0.0.8000/api/docs/ or http://127.0.0.8001/api/docs/ for docker-compose
<br>
Download it:
<br>
http://127.0.0.8000/api/schema/ or http://127.0.0.8001/api/schema/ for docker-compose
