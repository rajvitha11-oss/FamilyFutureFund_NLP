CREATE DATABASE  family_future_fund;

USE family_future_fund;

CREATE TABLE IF NOT EXISTS goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    goal_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    duration_months INT NOT NULL,
    monthly_saving DECIMAL(12,2) NOT NULL,
    saved_amount DECIMAL(12,2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'In Progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SHOW TABLES;


DESCRIBE goals;