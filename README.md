# 🧪 Data QA Portfolio — Интернет-магазин

> Учебный проект по тестированию данных. Проверка качества данных интернет-магазина: поиск дефектов в исходных таблицах и витрине данных после ETL.

---

## 📋 Описание проекта

В проекте есть три таблицы:
- `customers` — покупатели
- `orders` — заказы
- `dm_customer_summary` — витрина данных после ETL

**Задача:** найти все дефекты данных и написать SQL-запросы для автоматической проверки.

---

## 🗄️ Структура данных

### Таблица `customers`
```sql
customer_id | name          | age | email                | country
------------|---------------|-----|----------------------|--------
1           | Алия Иванова  | 28  | aliya@gmail.com      | KZ
2           | Марат Сейтов  | -3  | marat@gmail.com      | KZ
3           | Дана Ли       | 35  | dana_gmail.com       | RU
4           | Сергей Попов  | 30  | sergey@gmail.com     | XX
5           | Асель Нурова  | 22  | asel@gmail.com       | KZ
6           | Асель Нурова  | 22  | asel@gmail.com       | KZ
7           | Тимур Беков   | 200 | timur@gmail.com      | KZ
8           | NULL          | 25  | anna@gmail.com       | RU
```

### Таблица `orders`
```sql
order_id | customer_id | amount  | status    | created_at
---------|-------------|---------|-----------|------------
101      | 1           | 15000   | done      | 2024-01-15
102      | 2           | 8000    | done      | 2024-01-16
103      | 3           | -500    | done      | 2024-01-17
104      | 4           | 0       | done      | 2024-01-17
105      | 5           | 22000   | done      | 2024-01-18
106      | 5           | 22000   | done      | 2024-01-18
107      | 99          | 5000    | done      | 2024-01-19
108      | 1           | 3000    | shipped   | 2024-01-20
109      | 3           | 1500    | cancelled | 2024-01-21
```

### Витрина `dm_customer_summary`
```sql
customer_id | total_amount | order_count | last_status
------------|--------------|-------------|------------
1           | 18000        | 2           | shipped
2           | 8000         | 1           | done
3           | 500          | 1           | done
5           | 44000        | 2           | done
```

---

## 🐛 Чек-лист дефектов

| № | Таблица | Строка | Поле | Проблема | Тип дефекта |
|---|---------|--------|------|----------|-------------|
| 1 | customers | 2 | age | age = -3, возраст не может быть отрицательным | Недопустимое значение |
| 2 | customers | 3 | email | нет символа @, формат email неверный | Неверный формат |
| 3 | customers | 5, 6 | все поля | полный дубликат строки Асель Нуровой | Дубликат |
| 4 | customers | 7 | age | age = 200, возраст не может быть больше 120 | Недопустимое значение |
| 5 | customers | 4 | country | country = XX, такой страны не существует | Недопустимое значение |
| 6 | customers | 8 | name | name = NULL, имя обязательное поле | Пропущенное значение |
| 7 | orders | 3 | amount | amount = -500, сумма не может быть отрицательной | Недопустимое значение |
| 8 | orders | 4 | amount | amount = 0, сумма не может быть нулевой | Недопустимое значение |
| 9 | orders | 5, 6 | все поля | полный дубликат заказа customer_id = 5 | Дубликат |
| 10 | orders | 7 | customer_id | customer_id = 99 не существует в таблице customers | Нарушение ссылочной целостности |
| 11 | dm_customer_summary | 3 | total_amount | стоит 500 вместо -500 — ETL потерял знак | Неверная агрегация |
| 12 | dm_customer_summary | 4 | total_amount | стоит 44000 вместо 22000 — дубликат попал в витрину | Неверная агрегация |
| 13 | dm_customer_summary | — | customer_id | customer_id = 4 отсутствует в витрине | Потеря данных |
| 14 | dm_customer_summary | — | customer_id | customer_id = 6 отсутствует в витрине | Потеря данных |

**Итого найдено дефектов: 14**

---

## 🔍 SQL-запросы для проверки

### Проверка 1 — Недопустимый возраст
```sql
SELECT *
FROM customers
WHERE age < 1 OR age > 120;
```
**Ожидаемый результат:** строки 2 (age = -3) и 7 (age = 200)

---

### Проверка 2 — Дубликаты покупателей
```sql
SELECT email, COUNT(*) as cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```
**Ожидаемый результат:** asel@gmail.com — 2 записи

---

### Проверка 3 — Недопустимые суммы заказов
```sql
SELECT *
FROM orders
WHERE amount <= 0;
```
**Ожидаемый результат:** строки с amount = -500 и amount = 0

---

### Проверка 4 — Заказы без существующего покупателя
```sql
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```
**Ожидаемый результат:** order_id = 107, customer_id = 99

---

### Проверка 5 — Потеря данных в витрине
```sql
SELECT DISTINCT o.customer_id
FROM orders o
LEFT JOIN dm_customer_summary d ON o.customer_id = d.customer_id
WHERE d.customer_id IS NULL;
```
**Ожидаемый результат:** customer_id = 4 и customer_id = 6

---

### Проверка 6 — Дубликаты заказов
```sql
SELECT customer_id, amount, status, created_at, COUNT(*) as cnt
FROM orders
GROUP BY customer_id, amount, status, created_at
HAVING COUNT(*) > 1;
```
**Ожидаемый результат:** дубликат заказа customer_id = 5

---

### Проверка 7 — Сравнение витрины с источником
```sql
SELECT 
    o.customer_id,
    SUM(o.amount) as expected_total,
    d.total_amount as actual_total
FROM orders o
LEFT JOIN dm_customer_summary d ON o.customer_id = d.customer_id
WHERE o.status != 'cancelled'
GROUP BY o.customer_id, d.total_amount
HAVING SUM(o.amount) != d.total_amount;
```
**Ожидаемый результат:** расхождения для customer_id = 3 и customer_id = 5

---

## 🛠️ Инструменты
- SQL (SQLite / PostgreSQL)
- Python + pandas (для автоматического сравнения таблиц)

---

## 👤 Автор
Учебный проект в рамках освоения профессии Data QA Engineer.
```
Навыки: SQL, ETL-тестирование, тест-дизайн, поиск дефектов данных
```
