# LibraryProject

A simple Django project for managing a library system.

## Features

- Manage books, authors, and genres
- User authentication
- Book borrowing and returning
- Admin interface for easy management

## Requirements

- Python 3.8+
- Django 4.x

## Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd LibraryProject
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the site at `http://127.0.0.1:8000/`
- Admin interface at `http://127.0.0.1:8000/admin/`

## License

MIT License