import pandas as pd

# Создаём тестовые данные (наша таблица customers)
data = {
    'customer_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'name':        ['Алия', 'Марат', 'Дана', 'Сергей', 'Асель', 'Асель', 'Тимур', None],
    'age':         [28, -3, 35, 30, 22, 22, 200, 25],
    'email':       ['aliya@gmail.com', 'marat@gmail.com', 'dana_gmail.com',
                    'sergey@gmail.com', 'asel@gmail.com', 'asel@gmail.com',
                    'timur@gmail.com', 'anna@gmail.com'],
    'country':     ['KZ', 'KZ', 'RU', 'XX', 'KZ', 'KZ', 'KZ', 'RU']
}

df = pd.DataFrame(data)

print("=== Наша таблица ===")
print(df) 
# ПРОВЕРКА 1 — NULL значения
print("\n=== Проверка 1: NULL значения ===")
nulls = df[df['name'].isna()]
if len(nulls) > 0:
    print(f"БАГИ НАЙДЕНЫ: {len(nulls)} строк с пустым именем")
    print(nulls)
else:
    print("OK — пустых имён нет")
    # ПРОВЕРКА 2 — Дубликаты
print("\n=== Проверка 2: Дубликаты ===")
duplicates = df[df.duplicated(subset=['email'], keep=False)]
if len(duplicates) > 0:
    print(f"БАГИ НАЙДЕНЫ: {len(duplicates)} строк с одинаковым email")
    print(duplicates)
else:
    print("OK — дубликатов нет")
    # ПРОВЕРКА 3 — Недопустимый возраст
print("\n=== Проверка 3: Недопустимый возраст ===")
bad_age = df[(df['age'] < 1) | (df['age'] > 120)]
if len(bad_age) > 0:
    print(f"БАГИ НАЙДЕНЫ: {len(bad_age)} строк с неверным возрастом")
    print(bad_age)
else:
    print("OK — возраст в норме")
    # ПРОВЕРКА 4 — Неверный формат email
print("\n=== Проверка 4: Неверный формат email ===")
bad_email = df[~df['email'].str.contains('@', na=False)]
if len(bad_email) > 0:
    print(f"БАГИ НАЙДЕНЫ: {len(bad_email)} строк с неверным email")
    print(bad_email)
else:
    print("OK — все email в порядке")  
     # ПРОВЕРКА 5 — Недопустимая страна
print("\n=== Проверка 5: Недопустимая страна ===")
bad_country = df[df['country'] == 'XX']
if len(bad_country) > 0:
    print(f"БАГИ НАЙДЕНЫ: {len(bad_country)} строк с неверной страной")
    print(bad_country)
else:
    print("OK — все страны в порядке")
    total_bugs = len(nulls) + len(duplicates) + len(bad_age) + len(bad_email) + len(bad_country)

    # ИТОГОВЫЙ ОТЧЁТ
print("\n" + "="*40)
print("ИТОГОВЫЙ ОТЧЁТ ПРОВЕРКИ")
print("="*40)

total_bugs = len(nulls) + len(duplicates) + len(bad_age) + len(bad_email)

print(f"Всего строк проверено: {len(df)}")
print(f"NULL в именах:         {len(nulls)}")
print(f"Дубликаты:             {len(duplicates)}")
print(f"Неверный возраст:      {len(bad_age)}")
print(f"Неверный email:        {len(bad_email)}")
print(f"ИТОГО БАГОВ:           {total_bugs}")

if total_bugs > 0:
    print("\nСТАТУС: ТАБЛИЦА НЕ ПРОШЛА ПРОВЕРКУ ❌")
else:
    print("\nСТАТУС: ТАБЛИЦА ПРОШЛА ПРОВЕРКУ ✅")
   