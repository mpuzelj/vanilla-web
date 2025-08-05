# Tools

This folder contains helper scripts for the project.

---

## hash_password.py

**Purpose:**  
Generate a bcrypt hash for a password.  
Use this to create secure password hashes for inserting users directly into the database (e.g., in your `init.sql`).

**Usage:**

1. Run the script inside the Docker container with requirements:
   ```
   docker-compose run --rm web python /app/tools/hash_password.py
   ```
2. Enter the password you want to hash when prompted.
3. Copy the output hash and use it in your SQL scripts or admin tools.
