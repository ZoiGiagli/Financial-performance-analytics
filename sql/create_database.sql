
-- Financial Performance Analytics
-- Database setup (MySQL 8.0+)

CREATE DATABASE IF NOT EXISTS FinancialAnalytics;

USE FinancialAnalytics;

CREATE TABLE IF NOT EXISTS Sales (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    product VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    revenue DECIMAL(12,2) NOT NULL,
    cost DECIMAL(12,2) NOT NULL
);
