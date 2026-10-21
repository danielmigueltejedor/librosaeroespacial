SELECT customer_id, SUM(cents) AS total
FROM orders GROUP BY customer_id ORDER BY customer_id;
