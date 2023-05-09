CREATE USER 'stock'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE IF NOT EXISTS stockdb;
USE stockdb;
GRANT ALL PRIVILEGES ON stockdb.* TO 'stock'@'localhost';