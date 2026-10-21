SELECT c.id, COUNT(o.id) AS orders_count
FROM customer AS c LEFT JOIN orders AS o ON o.customer_id = c.id
GROUP BY c.id ORDER BY c.id;
