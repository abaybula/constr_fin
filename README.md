# Django Construction Financing Schedule

This project is a project for tracking construction financing. It allows users to add, view, and track construction
positions and their costs over time using a financing schedule.

## Requirements

- Python
- Django
- PostgreSQL
- Docker

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/abaybula/constr_fin.git
    cd constr_fin
    ```

2. Deployment with Docker:

    ```bash
    docker compose up --build
    ```

3. To create translation files, run and compile translation files:

    ```bash
    docker compose run --rm web-app sh -c "django-admin makemessages -l uk"
    docker compose run --rm web-app sh -c "django-admin compilemessages"
    ```

4. Collect static files:

    ```bash
    docker compose run --rm web-app sh -c "./manage.py collectstatic"
    ```

5. Set up the database in `settings.py`:

    ```python
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': '5432',
        }
    }
    ```

6. Run database migrations:

    ```bash
    docker compose run --rm web-app sh -c "./manage.py migrate"
    ```

7. Create a superuser:

    ```bash
    docker compose run --rm web-app sh -c "./manage.py createsuperuser"
    ```

8. Run the development server:

    ```bash
    docker compose up
    ```

## Usage

After starting the development server, open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser, register and
log in with the user account. Now you can add new construction positions, view them, and track costs using a financing
schedule.
