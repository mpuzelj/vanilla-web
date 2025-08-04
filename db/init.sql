CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Insert default admin user
INSERT INTO users (username, password, is_admin)
VALUES ('admin', 'admin', TRUE)
ON CONFLICT (username) DO NOTHING;