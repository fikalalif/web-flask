from flask import Flask, render_template, request, redirect,url_for,jsonify,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = ' Kanjut Store'
#KONFIGURASI DATABASE
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web1_3e'

mysql = MySQL(app)

@app.route('/cek database')
def cek_database():
    cur = mysql.connection.cursor()
    cur.execute('SELECT 1')
    return jsonify('message : database connected')

@app.route('/')
def home():
    name = 'ahhhh mantap'
    return render_template('index.html')

@app.route('/about')
def about():
    name = 'david jujul'
    age = 24
    buah =[]    
    
    produk = [
        {'name' : 'sepatu aero street', 'price' : 400000, 'stock' : True},
        {'name' : 'sepatu kulit kanjut', 'price' : 10000000000, 'stock' : True},
        {'name' : 'sepatu kompas', 'price' : 200000, 'stock' : False}
    ]

    return render_template('about.html', myname = name, myage = age, mybuah = buah, myproduk = produk)
    
@app.route('/homepage')
def homepage():
    cur = mysql.connection.cursor()
    query = '''SELECT product.*, category.name_category FROM product INNER JOIN category ON product.category = category.id_category'''
    #STRING TIGA BISA MENAMBAHKAN BEBERAPA KODE DITIAP BARIS NYA
    cur.execute(query)
    product = cur.fetchall()

    return render_template('home_page.html', product = product)


@app.route('/aboutpage')
def aboutpage():
    return render_template('about_page.html')

@app.route('/simpan-data', methods=['post'])
def submit():
    name_product = request.form['name_product'].upper()
    category = request.form['category']
    price = request.form['price']
    image_url = request.form['image_url']
    stok = request.form['stok']
    data = {
            'name' : name_product, 
            'category' : category, 
            'price' : price, 
            'image_url' : image_url,
            'stok' : stok,
            }
    database.append(data)
    return redirect(url_for('home'))    

@app.route('/form-product')
def form_add_product():
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM category'
    cur.execute(query)
    category = cur.fetchall()
    return render_template('form-product.html', category = category)

@app.route('/add-product', methods = ['POST'])
def add_product():
    #req data dari form
    name_product = request.form['name_product']
    image_url = request.form['image_url']
    price = request.form['price']
    category = request.form['category']
    in_stock = request.form['in_stock']

    if not name_product or len(name_product) < 2:
        flash('Inputan name product harus diisi','warning ')

    #menyimpan data ke tabel my sql
    cur = mysql.connection.cursor()
    query = 'INSERT INTO product(name_product, image_url, price, category, in_stock) VALUES (%s, %s, %s, %s, %s)'
    cur.execute(query,(name_product,image_url,price,category,in_stock))
    mysql.connection.commit()
    flash('data berhasil disimpan','succes')
    return redirect('/homepage')

@app.route('/form-edit-product/<int:id>')
def form_edit_product(id):
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM product WHERE id = %s'
    cur.execute(query, [id])
    product = cur.fetchone()
    # return jsonify (product)
    query = 'SELECT * FROM category'
    cur.execute(query)
    category = cur.fetchall()

    return render_template('form-edit-product.html' , product = product, category = category )

@app.route('/edit-product/<int:id>', methods = ['POST'])
def edit_product(id):
    #req data dari form
    name_product = request.form['name_product']
    image_url = request.form['image_url']
    price = request.form['price']
    category = request.form['category']
    in_stock = request.form['in_stock']

    #menyimpan data ke tabel my sql
    cur = mysql.connection.cursor()
    query = ''' UPDATE product SET 
                name_product = %s,
                image_url = %s,
                price = %s,
                category = %s,
                in_stock = %s
                WHERE id = %s
            '''
    cur.execute(query,(name_product,image_url,price,category,in_stock,id))
    mysql.connection.commit()
    flash('data berhasil diedit','succes')
    return redirect('/homepage')

@app.route('/delete-product/<int:id>')
def delete_product(id):
    cur = mysql.connection.cursor()
    query = 'DELETE FROM product WHERE id = %s'
    cur.execute(query, [id])
    mysql.connection.commit()
    flash ('Data Berhasil dihapus','succes')
    return redirect('/homepage')

