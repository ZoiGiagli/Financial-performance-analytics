
-- Financial Performance Analytics
-- Sales analysis queries (MySQL 8.0+)

USE FinancialAnalytics;

-- 1. Verify the number of transactions
SELECT COUNT(*) AS total_orders
FROM Sales;

-- 2. Overall financial KPIs
SELECT
    SUM(revenue) AS total_revenue,
    SUM(cost) AS total_cost,
    SUM(revenue) - SUM(cost) AS total_profit,
    ROUND(
        (SUM(revenue) - SUM(cost))
        / NULLIF(SUM(revenue), 0) * 100,
        2
    ) AS profit_margin
FROM Sales;

-- 3. Profit by product category
SELECT
    category,
    SUM(revenue - cost) AS total_profit
FROM Sales
GROUP BY category
ORDER BY total_profit DESC;

-- 4. Top 3 most profitable products
SELECT
    product,
    SUM(revenue - cost) AS total_profit
FROM Sales
GROUP BY product
ORDER BY total_profit DESC
LIMIT 3;

-- 5. Monthly revenue trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(revenue) AS total_revenue
FROM Sales
GROUP BY month
ORDER BY month;
