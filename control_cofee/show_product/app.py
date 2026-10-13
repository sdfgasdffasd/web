from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(r"C:\Users\kolka\OneDrive\Desktop\control_cofee\database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get company info (read-only, one row)
    company = conn.execute('SELECT * FROM company').fetchone()
    
    # Get all categories
    categories = conn.execute('SELECT * FROM category').fetchall()
    
    # Get all products
    products = conn.execute('SELECT * FROM product').fetchall()
    
    # Group products by category name
    categories_with_products = []
    for category in categories:
        category_products = [p for p in products if p['category'] == category['name']]
        categories_with_products.append({
            'id': category['id'],
            'name': category['name'],
            'products': category_products
        })
    
    conn.close()
    
    return render_template('index.html', 
                         company=company,
                         categories_with_products=categories_with_products)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
