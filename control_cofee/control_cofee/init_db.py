import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create manager table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manager (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create company table (single row with id=1)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY,
            user_name TEXT,
            link_image_brand TEXT,
            link_facebook TEXT,
            num_phone TEXT
        )
    ''')
    
    # Create category table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_product TEXT NOT NULL,
            price REAL NOT NULL,
            link_image TEXT,
            description TEXT,
            category TEXT
        )
    ''')
    
    # Insert default manager accounts
    cursor.execute('''
        INSERT OR IGNORE INTO manager (user_name, password) 
        VALUES ('covariance', 'Cpersonal_r')
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO manager (user_name, password) 
        VALUES ('cofee_place_damn', 'Cofee_oo_123')
    ''')
    
    # Insert default company row (id=1) with empty values
    cursor.execute('''
        INSERT OR IGNORE INTO company (id, user_name, link_image_brand, link_facebook, num_phone)
        VALUES (1, '', '', '', '')
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
