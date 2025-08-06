CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    login_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255)
);

-- Insert default admin user (active, no token needed)
INSERT INTO users (email, password, is_admin, is_active)
VALUES ('admin@admin.com', '$2b$12$haJzIT7XyADfg/dI56BNoOkq1ix3cURw.FdrsPR30q8O9H.iQciUm', TRUE, TRUE)
ON CONFLICT (email) DO NOTHING;
