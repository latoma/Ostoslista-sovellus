CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    "password" TEXT
);

CREATE TABLE shopping_lists (
    list_id SERIAL PRIMARY KEY,
    list_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table to manage the many-to-many relationship between users and shopping lists
CREATE TABLE user_shopping_lists (
    user_id INT NOT NULL,
    list_id INT NOT NULL,
    PRIMARY KEY (user_id, list_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (list_id) REFERENCES shopping_lists(list_id)
);