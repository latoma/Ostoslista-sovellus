CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    "password" TEXT
);

CREATE TABLE shopping_lists (
    list_id SERIAL PRIMARY KEY,
    list_name VARCHAR(100) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE item_lists (
    item_id SERIAL PRIMARY KEY,
    list_id INT NOT NULL,
    item_desc TEXT NOT NULL,
    FOREIGN KEY (list_id) REFERENCES shopping_lists(list_id)
);

CREATE TABLE shared_lists (
    share_id SERIAL PRIMARY KEY,
    shopping_list_id INT,
    user_id INT,
    FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists(list_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE (shopping_list_id, user_id)
);