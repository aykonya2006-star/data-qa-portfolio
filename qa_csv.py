import pandas as pd

# Загружаем CSV файл
df = pd.read_csv(r'C:\Users\Ravil\qu  training\customers.csv')

print("=== Файл загружен! ===")
print(f"Строк: {df.shape[0]}")
print(f"Колонок: {df.shape[1]}")
print("\nПервые 3 строки:")
print(df.head(3))
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
dupes = df[df.duplicated(subset=['email'], keep=False)]
if len(dupes) > 0:
    print(f"БАГИ НАЙДЕНЫ: {len(dupes)} строк с одинаковым email")
    print(dupes)
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

# ИТОГОВЫЙ ОТЧЁТ
print("\n" + "="*40)
print("ИТОГОВЫЙ ОТЧЁТ")
print("="*40)
total = len(nulls) + len(dupes) + len(bad_age)
print(f"Всего строк проверено: {len(df)}")
print(f"NULL в именах:         {len(nulls)}")
print(f"Дубликаты:             {len(dupes)}")
print(f"Неверный возраст:      {len(bad_age)}")
print(f"ИТОГО БАГОВ:           {total}")
if total > 0:
    print("СТАТУС: ❌ НЕ ПРОШЛА")
else:
    print("СТАТУС: ✅ ПРОШЛА")