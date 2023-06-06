DROP DATABASE IF EXISTS ressellr;
CREATE DATABASE ressellr;

CREATE OR REPLACE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON ressellr.* TO 'user'@'localhost';

USE ressellr;

CREATE TABLE users (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `token` VARCHAR(500),
    `username` VARCHAR(500) UNIQUE,
    `name` VARCHAR(500),
    `email` VARCHAR(500) UNIQUE,
    `avatar` VARCHAR(500) DEFAULT NULL,
    `rating` FLOAT DEFAULT 0.0,
    `total_sales` INT DEFAULT 0,
    `total_purchases` INT DEFAULT 0,
    `total_reviews` INT DEFAULT 0,
    `phone` INT UNIQUE,
    `registration` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `location` VARCHAR(500),
    `is_active` BOOLEAN DEFAULT TRUE
);


CREATE TABLE items (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(500) ,
    `date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `description` VARCHAR(500),
    `price` FLOAT,
    `old_price` FLOAT DEFAULT NULL,
    `image` VARCHAR(500),
    `location` VARCHAR(500),
    `condition` VARCHAR(500),
    `is_available` BOOLEAN DEFAULT TRUE,
    `owner_id` INT,
    `category_id` INT,
    `product_id` INT,
    FOREIGN KEY (owner_id) REFERENCES users(id)
    -- FOREIGN KEY (category_id) REFERENCES categories(id) -- uncomment for external database/table
    -- FOREIGN KEY (product_id) REFERENCES products(id) -- uncomment for external database/table
);


-- Insert random users
INSERT INTO users (token, username, name, email, avatar, rating, total_sales, total_purchases, total_reviews, phone, registration, location, is_active)
VALUES
    ('token1', 'user1', 'User One', 'user1@example.com', 'avatar1.jpg', 4.5, 10, 8, 12, 123456789, NOW(), 'Location 1', TRUE),
    ('token2', 'user2', 'User Two', 'user2@example.com', 'avatar2.jpg', 3.8, 5, 15, 6, 987654321, NOW(), 'Location 2', TRUE);

-- Insert random items
INSERT INTO items (title, date, description, price, old_price, image, location, condition, is_available, owner_id, category_id, product_id)
VALUES
    ('Item 1', NOW(), 'Description for Item 1', 50.99, 39.99, 'item1.jpg', 'Location 1', 'Good', TRUE, 1, 1, 1),
    ('Item 2', NOW(), 'Description for Item 2', 24.99, NULL, 'item2.jpg', 'Location 2', 'Excellent', TRUE, 1, 2, 2),
    ('Item 3', NOW(), 'Description for Item 3', 19.99, 16.99, 'item3.jpg', 'Location 1', 'Fair', TRUE, 2, 1, 1),
    ('Item 4', NOW(), 'Description for Item 4', 99.99, 89.99, 'item4.jpg', 'Location 2', 'Good', TRUE, 2, 2, 2);
