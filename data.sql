-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    district TEXT NOT NULL,
    role TEXT NOT NULL
);

-- Incidents table
CREATE TABLE incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    district TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'Open', -- Added Default here
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

