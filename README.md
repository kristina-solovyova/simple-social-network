# Simple social network
Implementation of simple REST API using Django and Django REST framework.

**Swagger** (OpenAPI):  
https://social-net-api.herokuapp.com/openapi  

**Basic models:**
* User
* Post

**Basic features:**
* user signup
* user login
* post creation
* post like
* post unlike
* user follow
* user unfollow

### Prerequisites
* Python3
* virtualenv
* PostgreSQL database (or just use SQLite for testing)

### Installation

Clone repository:
```bash
git clone https://github.com/kristina-solovyova/simple-social-network.git
cd simple-social-network
```

Create and activate virtual environment, install requirements:
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Create `.env` file in project root folder and add environment variables:
```
SECRET_KEY=generate_new_secret_key
DATABASE_URL=local_database_url
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1
```

Apply existing migrations and run server:
```
python manage.py migrate
python manage.py runserver
```
