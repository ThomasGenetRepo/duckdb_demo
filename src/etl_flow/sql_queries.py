# import csv data
import_customers = """
    CREATE OR REPLACE TABLE raw_customers AS SELECT * FROM read_csv_auto('/data/raw/raw_customers.csv');
"""
import_orders = """
    CREATE OR REPLACE TABLE raw_orders AS SELECT * FROM read_csv_auto('/data/raw/raw_orders.csv');
"""
import_product = """
    CREATE OR REPLACE TABLE raw_product AS SELECT * FROM read_csv_auto('/data/raw/raw_products.csv');
"""

# do the transformations
spending_by_customer = """
CREATE OR REPLACE TABLE spending_per_customer AS
SELECT o.customer_id, SUM(o.price * o.quantity) as total_spent
FROM raw_orders o
GROUP BY o.customer_id;
"""

customer_segmentation = """
CREATE OR REPLACE TABLE CustomerSegmentation AS
SELECT customer_id, 
CASE 
    WHEN total_spent > 60 THEN 'High'
    WHEN total_spent > 50 THEN 'Medium'
    ELSE 'Low'
END AS spending_category
FROM spending_per_customer;
"""

inventory_level = """
CREATE OR REPLACE TABLE InventoryLevel AS
SELECT product, 
CASE 
    WHEN stock_quantity < 60 THEN 'Low'
    WHEN stock_quantity < 100 THEN 'Medium'
    WHEN stock_quantity < 140 THEN 'High'
    ELSE 'Overstocked'
END AS inventory_level
FROM raw_product;
"""

customer_lifetime_value = """
CREATE OR REPLACE TABLE CustomerLifetimeValue AS
SELECT customer_id, total_spent * 2 / (1 + 0.1) as clv
FROM spending_per_customer;
"""

product_review = """
CREATE OR REPLACE TABLE ProductRevenue AS
SELECT product, SUM(quantity * price) as revenue
FROM raw_orders
GROUP BY product;
"""

frequent_customer = """
CREATE OR REPLACE TABLE FrequentCustomers AS
SELECT customer_id, COUNT(order_id) as order_count
FROM raw_orders
GROUP BY customer_id
HAVING COUNT(order_id) > 2;
"""