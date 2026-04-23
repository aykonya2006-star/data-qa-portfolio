-- ============================================
-- Data QA проверки: Интернет-магазин
-- Автор: Junior Data QA Engineer
-- ============================================

-- ПРОВЕРКА 1: Недопустимый возраст (должен быть от 1 до 120)
SELECT *
FROM customers
WHERE age < 1 OR age > 120;
-- Ожидаем: age = -3 (Марат), age = 200 (Тимур)

-- ПРОВЕРКА 2: Дубликаты покупателей
SELECT email, COUNT(*) as cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
-- Ожидаем: asel@gmail.com — 2 записи

-- ПРОВЕРКА 3: Пропущенные имена покупателей
SELECT *
FROM customers
WHERE name IS NULL;
-- Ожидаем: строка 8 (anna@gmail.com)

-- ПРОВЕРКА 4: Недопустимые суммы заказов
SELECT *
FROM orders
WHERE amount <= 0;
-- Ожидаем: amount = -500 и amount = 0

-- ПРОВЕРКА 5: Заказы без существующего покупателя
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
-- Ожидаем: order_id = 107, customer_id = 99

-- ПРОВЕРКА 6: Дубликаты заказов
SELECT customer_id, amount, status, created_at, COUNT(*) as cnt
FROM orders
GROUP BY customer_id, amount, status, created_at
HAVING COUNT(*) > 1;
-- Ожидаем: дубликат заказа customer_id = 5

-- ПРОВЕРКА 7: Потеря данных в витрине
SELECT DISTINCT o.customer_id
FROM orders o
LEFT JOIN dm_customer_summary d ON o.customer_id = d.customer_id
WHERE d.customer_id IS NULL;
-- Ожидаем: customer_id = 4 и customer_id = 6

-- ПРОВЕРКА 8: Сравнение витрины с источником
SELECT
    o.customer_id,
    SUM(o.amount) as expected_total,
    d.total_amount as actual_total
FROM orders o
LEFT JOIN dm_customer_summary d ON o.customer_id = d.customer_id
WHERE o.status != 'cancelled'
GROUP BY o.customer_id, d.total_amount
HAVING SUM(o.amount) != d.total_amount;
-- Ожидаем: расхождения для customer_id = 3 и customer_id = 5
