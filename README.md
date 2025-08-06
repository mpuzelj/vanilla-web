# Vanilla Web Project

## Overview

This project is:
- a simple web application with user registration, email verification, and admin tools
- it uses Docker Compose to orchestrate all required services
- includes Postgres DB, pgAdmin and Mailhog mock email server

---

## Project Structure

```
C:.
│   docker-compose.yml
│   README.md
│
├───db
│       init.sql
│
├───pgadmin
│       servers.json
│
├───tools
│       hash_password.py
│       README.md
│
└───web
    │   app.py
    │   Dockerfile
    │   requirements.txt
    │
    ├───static
    │       style.css
    │
    ├───templates
    │       admin.html
    │       index.html
    │       login.html
    │       register.html
    │
    └───tools
```

---

## Components (Docker Compose Services)

- **db**: PostgreSQL database (`admin`/`admin`), initialized with `db/init.sql`.
- **web**: Flask application (user registration, login, email verification, admin console).
- **pgadmin**: pgAdmin 4 web-based database management tool.
- **mailhog**: MailHog mock SMTP server for capturing outgoing emails (viewable in web UI).

---

## Prerequisites

### Windows

- [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) (Windows Package Manager)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  ```
  winget install --id Docker.DockerDesktop -e
  ```
- [Git](https://git-scm.com/)
  ```
  winget install --id Git.Git -e
  ```

### Linux

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

---

## How to Start

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd vanilla-web
   ```

2. **Start all services:**
   ```
   docker-compose up --build
   ```

3. **Access the components:**
   - **Admin Console:** [http://localhost:5000/admin](http://localhost:5000/admin)
   - **Web app:** [http://localhost:5000](http://localhost:5000)
   - **pgAdmin:** [http://localhost:5050](http://localhost:5050)
   - **MailHog:** [http://localhost:8025](http://localhost:8025)

---

## Default Login Data

- **Web Admin User:**  
  Email: `admin@admin.com`  
  Password: `admin`  
  (You may need to verify the password hash in `db/init.sql`.)

- **pgAdmin:**  
  Username (email): `admin@admin.com`  
  Password: `admin`

---

## Notes

- Registration requires email verification. All verification emails are captured by MailHog.
- pgAdmin is pre-configured to connect to the database.
- For development, all passwords and secrets are set to defaults. Change them for production use.

---
