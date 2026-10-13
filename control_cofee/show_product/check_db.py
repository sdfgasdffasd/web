import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

with open('db_output.txt', 'w', encoding='utf-8') as f:
    f.write('=== Company ===\n')
    cursor.execute('SELECT * FROM company')
    company_data = cursor.fetchall()
    f.write(f'Count: {len(company_data)}\n')
    f.write(str(company_data) + '\n\n')

    f.write('=== Category ===\n')
    cursor.execute('SELECT * FROM category')
    category_data = cursor.fetchall()
    f.write(f'Count: {len(category_data)}\n')
    f.write(str(category_data) + '\n\n')

    f.write('=== Product ===\n')
    cursor.execute('SELECT * FROM product')
    product_data = cursor.fetchall()
    f.write(f'Count: {len(product_data)}\n')
    f.write(str(product_data) + '\n\n')

    f.write('=== Manager (should not be used) ===\n')
    cursor.execute('SELECT * FROM manager')
    manager_data = cursor.fetchall()
    f.write(f'Count: {len(manager_data)}\n')
    for row in manager_data:
        f.write(f'ID: {row[0]}, Username: {row[1]} (password hidden)\n')

conn.close()
print('Database info written to db_output.txt')
