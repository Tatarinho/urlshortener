# URL Shortener Web Application

This project is a simple URL shortening service built using Django and Django Rest Framework (DRF). The service allows users to encode long URLs into shorter ones and decode shortened URLs back to their original form. The project is built with Python and includes a REST API with endpoints for encoding and decoding URLs.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Bonus Features](#bonus-features)
- [Project Structure](#project-structure)

## Features

- **Encode URL**: Convert a long URL into a shortened URL.
- **Decode URL**: Convert a shortened URL back into the original URL.
- **Database Storage**: Store URLs in a SQLite database.
- **REST API**: Simple and clean API for interacting with the service.
- **Unit Tests**: API tests using pytest.

## Prerequisites

- `Python 3.x` installed ( tested with Python 3.12.5 )
- `pip` package manager installed
- `virtualenv` installed (optional but recommended)

## Installation

### 1. Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

Apply the migrations:

```bash
python manage.py migrate
```

### 5. Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

Your application will be running at \`http://127.0.0.1:8000/`.

## Usage

### API Endpoints

### API Endpoints

- **Encode URL**

  - **Endpoint**: `/encode/`
  - **Method**: `POST`
  - **Request**:
    ```json
    {
      "url": "https://example.com/some-long-url"
    }
    ```
  - **Response**:
    ```json
    {
      "url": "http://127.0.0.1:8000/abc123"
    }
    ```
  
  - ** Example **:
    ```bash
    curl --location 'http://127.0.0.1:8000/encode/' \
    --header 'Content-Type: application/json' \
    --data '{
        "url": "https://www.youtube.com/watch?v=u15tEo0wsQI"
    }'
    ```

- **Decode URL**

  - **Endpoint**: `/decode/<str:short_code>/`
  - **Method**: `GET`
  - **Response**:
    ```json
    {
      "url": "https://example.com/some-long-url"
    }
    ```
  - ** Example **:
    ```bash
    curl --location 'http://127.0.0.1:8000/decode/017da475'
    ```

- **Process URL**

  - **Endpoint**: `/process/`
  - **Method**: `POST`
  - **Request**:
    ```json
    {
      "input_value": "https://example.com/some-long-url"
    }
    ```
  - **Response**:
    ```json
    {
      "url": "http://127.0.0.1:8000/abc123"
    }
    ```

- **Redirect URL**

  - **Endpoint**: `/<str:short_code>/`
  - **Method**: `GET`
  - **Response**: Redirects to the original URL.

## Testing

To run the tests using pytest, ensure pytest is installed, and then execute the following command:

```bash
pytest
```

This will discover and run all the tests defined in the project.

## Bonus Features

- **SQLite Database**: URLs can be persisted using SQLite.
- **Simple Web UI**: A basic UI for encoding and decoding URLs.

## Project Structure

```
urlshortener/
│
├── apps/                # Directory for Django apps
│   ├── __init__.py
│   ├── shortener/       # Django app for URL shortener
│   │   ├── migrations/  # Database migrations
│   │   ├── templates/   # Templates for the web UI
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py    # URL model
│   │   ├── tests.py     # Unit tests
│   │   ├── urls.py      # App URLs
│   │   ├── utils.py     # Utility functions
│   │   └── views.py     # Views and API logic
│
├── urlshortener/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py      # Django settings
│   ├── urls.py          # Project URLs
│   └── wsgi.py
│
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── Readme.md            # Project documentation
├── .flake8              # Flake8 configuration
├── mypy.ini             # MyPy configuration
└── pytest.ini           # Pytest configuration

```
