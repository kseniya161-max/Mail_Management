# Mail Management System

## Description

This project is a backend web application for managing clients and automated email campaigns.

Users can create, view, update, and delete clients and messages. Managers have extended permissions, including the ability to disable mailings.

The project also provides a REST API built with Django REST Framework (DRF) for managing core entities such as clients, products, categories, and mailings.

Additionally, the system supports:

* Email sending via SMTP and external Email APIs (Resend, Brevo)
* Generation of Excel files based on selected products (OpenPyXL)
* Attaching generated files to messages and mailings

The project demonstrates the development of a backend system for automating business workflows, including email campaigns and dynamic offer generation.

---

## Deployment

The project is deployed on Render (free tier).

* The service may go to sleep after ~15 minutes of inactivity
* The first request after inactivity may take 30–60 seconds

## CI (Continuous Integration)

The project uses GitHub Actions for CI.

On every push and pull request:

* tests are executed (pytest)
* code is checked with flake8
* formatting is validated with black
* environment is provisioned with PostgreSQL

This ensures code quality and stability across environments.

### Background processing

* Locally: Celery + Redis for asynchronous mailing
* Production (Render free tier): synchronous fallback (no worker)

---

## Features

### Client Management

* Create, view, update, and delete clients

### Message Management

* Create and manage messages
* Attach generated Excel files

### Mailing System

* Create mailings
* Send emails to selected recipients
* Disable mailings (manager role)

### User Management

* Authentication and registration
* Profile management
* Role-based access (user / manager)

---

## REST API

Endpoints available for:

* `/api/clients/`
* `/api/products/`
* `/api/categories/`
* `/api/mailings/`

Features:

* CRUD operations
* Authentication
* Role-based permissions
* Filtering

---

## File Generation & Email Integration

* Excel file generation (OpenPyXL)
* Email sending via:

  * SMTP
  * Resend API
  * Brevo API
* Support for file attachments

---

## Background Tasks

* Celery + Redis for async processing
* Fallback to synchronous execution if Celery is unavailable

---

## API Documentation

* Swagger: `/api/docs/`
* ReDoc: `/api/redoc/`
* Schema: `/api/schema/`

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis

* OpenPyXL
* Resend API
* Brevo API

* pytest
* pytest-django
* unittest.mock

* flake8
* black

* GitHub Actions (CI)

* Render
* WhiteNoise
* Pillow

---

## Testing

Unit tests cover core business logic:

* file generation (`file_service`)
* mailing logic (`mailing_service`)

Tools:

* pytest
* pytest-django
* unittest.mock

Features:

* database testing (`@pytest.mark.django_db`)
* mocking external APIs
* validation of DB records and logic

Run tests:

```bash
pytest
```

---

## Running the Project

After starting the server, the application is available at:

- Web interface: `http://127.0.0.1:8000/`
- API root: `http://127.0.0.1:8000/api/`
- DRF login: `http://127.0.0.1:8000/api-auth/login/`

Note: In production, the project is deployed on Render.

---

