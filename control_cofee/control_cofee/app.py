from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM manager WHERE user_name = ? AND password = ?', (username, password))
        manager = cursor.fetchone()
        conn.close()
        
        if manager:
            session['logged_in'] = True
            session['user_name'] = username
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('products'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('products'))
    return redirect(url_for('login'))

@app.route('/products')
@login_required
def products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product ORDER BY id DESC')
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name_product']
        price = request.form['price']
        link_image = request.form.get('link_image', '')
        description = request.form.get('description', '')
        category = request.form['category']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO product (name_product, price, link_image, description, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, link_image, description, category))
        conn.commit()
        conn.close()
        
        flash('تم إضافة المنتج بنجاح', 'success')
        return redirect(url_for('products'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM category ORDER BY name')
    categories = cursor.fetchall()
    conn.close()
    
    return render_template('product_form.html', categories=categories, action='add')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name_product']
        price = request.form['price']
        link_image = request.form.get('link_image', '')
        description = request.form.get('description', '')
        category = request.form['category']
        
        cursor.execute('''
            UPDATE product 
            SET name_product=?, price=?, link_image=?, description=?, category=?
            WHERE id=?
        ''', (name, price, link_image, description, category, id))
        conn.commit()
        conn.close()
        
        flash('تم تعديل المنتج بنجاح', 'success')
        return redirect(url_for('products'))
    
    cursor.execute('SELECT * FROM product WHERE id = ?', (id,))
    product = cursor.fetchone()
    cursor.execute('SELECT name FROM category ORDER BY name')
    categories = cursor.fetchall()
    conn.close()
    
    return render_template('product_form.html', product=product, categories=categories, action='edit')

@app.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('products'))

@app.route('/company')
@login_required
def company():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM company WHERE id = 1')
    company = cursor.fetchone()
    conn.close()
    return render_template('company.html', company=company)

@app.route('/company/edit', methods=['GET', 'POST'])
@login_required
def edit_company():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        user_name = request.form.get('user_name', '')
        link_image_brand = request.form.get('link_image_brand', '')
        link_facebook = request.form.get('link_facebook', '')
        num_phone = request.form.get('num_phone', '')
        
        cursor.execute('''
            UPDATE company 
            SET user_name=?, link_image_brand=?, link_facebook=?, num_phone=?
            WHERE id=1
        ''', (user_name, link_image_brand, link_facebook, num_phone))
        conn.commit()
        conn.close()
        
        flash('تم تعديل بيانات الشركة بنجاح', 'success')
        return redirect(url_for('company'))
    
    cursor.execute('SELECT * FROM company WHERE id = 1')
    company = cursor.fetchone()
    conn.close()
    
    return render_template('company.html', company=company, edit_mode=True)

@app.route('/categories')
@login_required
def categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, COUNT(p.id) as product_count
        FROM category c
        LEFT JOIN product p ON c.name = p.category
        GROUP BY c.id
        ORDER BY c.name
    ''')
    categories = cursor.fetchall()
    conn.close()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    name = request.form['name']
    
    if not name:
        flash('اسم النوع مطلوب', 'error')
        return redirect(url_for('categories'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO category (name) VALUES (?)', (name,))
        conn.commit()
        flash('تم إضافة النوع بنجاح', 'success')
    except sqlite3.IntegrityError:
        flash('هذا النوع موجود بالفعل', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('categories'))

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        new_name = request.form['name']
        
        if not new_name:
            flash('اسم النوع مطلوب', 'error')
            conn.close()
            return redirect(url_for('categories'))
        
        cursor.execute('SELECT name FROM category WHERE id = ?', (id,))
        old_name = cursor.fetchone()['name']
        
        try:
            # Update all products with this category name
            cursor.execute('UPDATE product SET category = ? WHERE category = ?', (new_name, old_name))
            # Update the category name itself
            cursor.execute('UPDATE category SET name = ? WHERE id = ?', (new_name, id))
            conn.commit()
            flash('تم تعديل النوع بنجاح', 'success')
        except sqlite3.IntegrityError:
            flash('هذا الاسم موجود بالفعل', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('categories'))
    
    cursor.execute('SELECT * FROM category WHERE id = ?', (id,))
    category = cursor.fetchone()
    conn.close()
    
    return render_template('categories.html', category=category, edit_mode=True)

@app.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if category has products
    cursor.execute('SELECT name FROM category WHERE id = ?', (id,))
    category_name = cursor.fetchone()['name']
    
    cursor.execute('SELECT COUNT(*) as count FROM product WHERE category = ?', (category_name,))
    count = cursor.fetchone()['count']
    
    if count > 0:
        flash(f'لا يمكن حذف هذا النوع لأنه مستخدم في {count} منتج، غيّر نوع هذه المنتجات أولاً', 'error')
    else:
        cursor.execute('DELETE FROM category WHERE id = ?', (id,))
        conn.commit()
        flash('تم حذف النوع بنجاح', 'success')
    
    conn.close()
    return redirect(url_for('categories'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
