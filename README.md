# Vanilla Web Project

## Overview

This project is:
- a simple web application with user registration, email verification, and admin tools
- it uses Docker Compose to orchestrate all required services locally
- includes Postgres DB, pgAdmin and Mailhog mock email server

---

## Project Structure

```
│   docker-compose.yml
│   LICENSE.md
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
    │       normalize.css
    │       skeleton.css
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

## Styling

This project uses [Skeleton CSS] for minimal default styling.  
- `normalize.css` is used for cross-browser consistency.
- `skeleton.css` provides a clean, responsive base.
- `style.css` contains custom overrides and tweaks.

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
   # Clone the repository
   git clone https://github.com/mpuzelj/vanilla-web.git
   # Move into the project folder
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

## Third-Party Licenses & Acknowledgements

This project uses the following open-source components:

- [Skeleton CSS](https://github.com/dhg/Skeleton) — MIT License
- [MailHog](https://github.com/mailhog/MailHog) — MIT License
- [PostgreSQL](https://www.postgresql.org/) — PostgreSQL License
- [pgAdmin](https://www.pgadmin.org/) — PostgreSQL Licence
- [Python](https://www.python.org/) — Python Software Foundation License
- [Flask](https://flask.palletsprojects.com/) — BSD License

Please refer to each project's website for full license details.
