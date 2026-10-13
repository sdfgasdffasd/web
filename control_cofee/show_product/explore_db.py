import sqlite3

conn = sqlite3.connect(r"C:\Users\kolka\OneDrive\Desktop\control_cofee\database.db")
cursor = conn.cursor()

# Get all tables
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [row[0] for row in cursor.fetchall()]
print('Tables:', tables)

# Explore company table
print('\n=== Table: company ===')
cursor.execute('PRAGMA table_info(company)')
columns = cursor.fetchall()
print('Columns:', columns)
cursor.execute('SELECT * FROM company')
rows = cursor.fetchall()
print('Data:', rows)

# Explore category table
print('\n=== Table: category ===')
cursor.execute('PRAGMA table_info(category)')
columns = cursor.fetchall()
print('Columns:', columns)
cursor.execute('SELECT * FROM category')
rows = cursor.fetchall()
print('Data:', rows)

# Explore product table
print('\n=== Table: product ===')
cursor.execute('PRAGMA table_info(product)')
columns = cursor.fetchall()
print('Columns:', columns)
cursor.execute('SELECT * FROM product')
rows = cursor.fetchall()
print('Data:', rows)

conn.close()
