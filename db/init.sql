CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    login_count INTEGER DEFAULT 0
);

-- Insert default admin user
INSERT INTO users (username, password, is_admin)
VALUES ('admin', '$2b$12$haJzIT7XyADfg/dI56BNoOkq1ix3cURw.FdrsPR30q8O9H.iQciUm', TRUE)
ON CONFLICT (username) DO NOTHING;
