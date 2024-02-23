CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

-- Table for shopping lists
CREATE TABLE shopping_lists (
    list_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    list_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
