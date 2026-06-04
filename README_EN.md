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

Recently added:

* Dedicated "My Offers" page for managing generated Excel files
* File deletion functionality
* User-level filtering of offer files in forms and views
---

## Deployment

The project is deployed on Render (free tier).

* The service may go to sleep after ~15 minutes of inactivity
* The first request after inactivity may take 30–60 seconds

## Environment Variables

Required:

- `RESEND_API_KEY`
- `RESEND_FROM_EMAIL`
- `DATABASE_URL`
- `SECRET_KEY`
- `DEBUG`

Optional:

- `USE_CELERY=True/False`

## Migrations

Django migrations are used for schema changes.  
Production considerations:
- Checking existing data before `null=False`
- Safe modification of nullable / non-nullable fields
- Data cleansing before schema migrations

## CI (Continuous Integration)

The project uses GitHub Actions for CI.

On every push and pull request:

* tests are executed (pytest)
* code is checked with flake8
* formatting is validated with black
* environment is provisioned with PostgreSQL

This ensures code quality and stability across environments.

---

## Email Delivery & Domain Authentication

To improve deliverability and avoid spam folders, the project implements:

- **SPF (Sender Policy Framework)** – authorises Resend / Amazon SES to send emails on behalf of the domain.  
  Example DNS record: `v=spf1 include:amazonses.com ~all`

- **DKIM (DomainKeys Identified Mail)** – cryptographically signs outgoing emails.  
  Configured via Resend as a TXT record (`resend._domainkey`).

- **DMARC (Domain-based Message Authentication, Reporting & Conformance)** – defines a policy and provides reporting.  
  Example record: `v=DMARC1; p=none;`

Email sending is provided by Resend API (primary) and Brevo API (fallback).  
Attachments (`.docx`, `.xlsx`) are supported via base64 encoding.

## System Design Overview

The project follows an asynchronous backend architecture:

- Task queue system (Celery + Redis)
- Email delivery pipeline
- Document generation pipeline
- Hybrid sync/async execution model
- External API integrations (email providers)

Business logic, background tasks, and external services are separated into distinct layers.

## Features

### Client Management

* Create, view, update, and delete clients
* Client detail page with contact information and quick actions.
* Excel offer generation for a specific client. 
* Generated offer files can be linked to a client and viewed in the client’s offer history.

### Message Management

* Create and manage messages
* Attach generated Excel files
* Select only user-specific generated files when attaching offers

### Mailing System

* Create mailings
* Send emails to selected recipients
* Disable mailings (manager role)

### Email Statistics

Implemented email campaign analytics:

* aggregation by mailings
* statistics by product categories
* role-based access control (manager / user)
* tracking successful and failed delivery attempts

Built using Django ORM:
* annotate()
* values()
* aggregations (Sum)
* relational queries using __ (JOIN-like behavior)

* analytical queries (group by / aggregation)

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
  * View generated files in a dedicated "My Offers" page
  * Delete previously generated offer files
  * User-specific access to generated files (each user sees only their own files)

---

## Background Processing System (Celery + Redis)

The project uses Celery for distributed task processing.  
**Monitoring**: Flower (run `celery -A config flower`)

### Task Types

1. **Email processing pipeline**  
   - Sending mailings, invoices, offer files  
   - Retry mechanism with exponential backoff  
   - Sync fallback mode (when Celery is disabled)

2. **Document generation pipeline**  
   - Excel offer generation  
   - DOCX invoice generation  
   - File storage in media directory

3. **Scheduler / automation**  
   - Periodic check of scheduled mailings  
   - Automatic campaign start

### Queue Architecture (Routing)

- `email_queue` – all email operations  
- `documents_queue` – file generation  
- `scheduler_queue` – periodic tasks

### Reliability & Fault Tolerance

- `max_retries` + `countdown` for failing tasks  
- `autoretry_for` for email tasks  
- Idempotent task design  
- Exception logging and fallback handling

### Hybrid Execution Model

- **Async mode** (Celery enabled) – default for local development  
- **Sync fallback mode** (Celery disabled) – for production environments without a worker (Render free tier)

This allows the system to run even without a full Celery infrastructure.

---

## API Documentation

* Swagger: `/api/docs/`
* ReDoc: `/api/redoc/`
* Schema: `/api/schema/`

---


## Logging System

Centralised logging is implemented using Python’s `logging` module.

### Covered Areas

- **Business events** – client creation, mailing creation, offer/invoice generation, email sending  
- **Background processing** – task start/end, retries, errors  
- **Email delivery pipeline** – success, fallback attempts, integration errors (Resend/Brevo)  
- **Error tracking** – missing files, missing client emails, document generation failures

### Log Levels

- `INFO` – successful business operations  
- `WARNING` – invalid user actions  
- `ERROR` – operation failures  
- `CRITICAL` – fallback failures (email delivery)

Logs are written to a rotating file (`logs/app.log`) and also output to the console for development.

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis
* Flower (monitoring)
* Docker
* Gunicorn
* Nginx

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

## Installation

1. Clone the repository:  
   `git clone https://github.com/kseniya161-max/Mail_Management.git`
2. Install dependencies:  
   `poetry install`
3. Activate the virtual environment:  
   `poetry shell`
4. Run migrations:  
   `python manage.py migrate`
5. Start the server:  
   `python manage.py runserver`

### Running background tasks

- Start Redis: `redis-server`
- Start Celery worker: `celery -A config worker --loglevel=info --pool=solo`

For async mode, set `USE_CELERY=True` in your environment.


## Containerization (Docker)

The project is fully containerized using Docker and Docker Compose.  
You need Docker Desktop installed and running.

For local development and testing, run:

```bash
docker-compose up -d --build
```

The following services are included:

* app – Django application (CRM)

* db – PostgreSQL (database)

* redis – Redis (broker for Celery and cache)

* celery_worker – Celery worker for background tasks

* celery_beat – Celery beat for periodic tasks

After startup, apply migrations and create a superuser:

```bash
docker-compose exec app python manage.py migrate
```
```bash
docker-compose exec app python manage.py createsuperuser
```
The site will be available at http://localhost:8000.

Stop all containers:

```bash
docker-compose down
```
To perform a full cleanup (including database and Redis volumes):
```bash
docker-compose down -v
```

### Production build (Gunicorn + Nginx)

For deploying the project to a server (e.g., Timeweb Cloud), a separate `docker-compose.prod.yml` file is used. It includes:
- **Gunicorn** instead of the built‑in `runserver`.
- **Nginx** as a reverse proxy to serve static and media files.

The required files are already included in the repository:
- `docker-compose.prod.yml` – production environment configuration.
- `nginx.conf` – Nginx web server configuration.

#### Preparation (locally or on the server)

1. Make sure environment variables are set (especially `SECRET_KEY`, `POSTGRES_PASSWORD` and `DEBUG=False`).
2. Collect static files:
   ```bash
   docker-compose -f docker-compose.prod.yml run --rm app python manage.py collectstatic --noinput
   ```
- Start the production stack:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
- Apply migrations if needed:
```bash
docker-compose -f docker-compose.prod.yml exec app python manage.py migrate
```

## Running the Project

After starting the server, the application is available at:

- Web interface: `http://127.0.0.1:8000/`
- API root: `http://127.0.0.1:8000/api/`
- DRF login: `http://127.0.0.1:8000/api-auth/login/`

### Running Celery with Flower

```bash
celery -A config flower --port=5555
```
Then open http://localhost:5555 to monitor queues and tasks.

Note: In production, the project is deployed on Render.

---

