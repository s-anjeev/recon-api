-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS recon_api_database;

-- Use the created database
USE recon_api_database;

-- Create the Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(10) DEFAULT 'admin',
    status ENUM('active', 'inactive') DEFAULT 'inactive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- Creating table to keep track of output files --
CREATE TABLE IF NOT EXISTS output_file_maping (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    command VARCHAR(128),
    output_file VARCHAR(128),
    timestamp VARCHAR(128)

);