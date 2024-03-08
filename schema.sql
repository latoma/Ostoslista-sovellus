CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    "password" TEXT
);

CREATE TABLE shopping_lists (
    list_id SERIAL PRIMARY KEY,
    list_name VARCHAR(50) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE list_items (
    item_id SERIAL PRIMARY KEY,
    list_id INT NOT NULL,
    item_desc VARCHAR(50) NOT NULL,
    FOREIGN KEY (list_id) REFERENCES shopping_lists(list_id)
);

CREATE TABLE ideas (
    idea_id SERIAL PRIMARY KEY,
    idea_name VARCHAR(50) NOT NULL,
    user_id INT,
    description VARCHAR(255)
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE idea_items (
    idea_item_id SERIAL PRIMARY KEY,
    idea_id INT NOT NULL,
    item_desc VARCHAR(50) NOT NULL,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);
