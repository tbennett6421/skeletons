SELECT COUNT(*)
FROM (
    SELECT
        c.name,
        c.customer_id,
    FROM master.customers c
);
