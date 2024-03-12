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

CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(50) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE recipe_items (
    item_id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    item_desc VARCHAR(50) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

CREATE TABLE shared_lists (
    shared_id SERIAL PRIMARY KEY,
    list_id INT,
    username VARCHAR(50),
    FOREIGN KEY (list_id) REFERENCES shopping_lists(list_id),
    FOREIGN KEY (username) REFERENCES users(username)
);