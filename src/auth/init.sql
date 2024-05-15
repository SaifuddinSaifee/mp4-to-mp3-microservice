-- Create a new user 'auth_user' with a password 'auth_user'
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth_user';

-- Create a new database named 'auth'
CREATE DATABASE auth;

-- Grant all privileges on the 'auth' database to 'auth_user'
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- Use the 'auth' database
USE auth;

-- Create a 'users' table with 'id', 'email', and 'password' fields
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert sample data into the 'users' table
INSERT INTO users (email, password) VALUES
('johndoe@email.com', 'johndoe123'),
('maria@email.com', 'maria123'),
('pedro@email.com', 'pedro123');
