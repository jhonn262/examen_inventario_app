from flask import Flask, render_template, request, redirect, url_for
from models import get_db_connection

app = Flask(__name__)

# Ruta principal: Listar productos
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Mostrar formulario para nuevo producto
@app.route('/nuevo', methods=['GET'])
def nuevo_producto_form():
    return render_template('nuevo_producto.html')

# Procesar nuevo producto
@app.route('/crear', methods=['POST'])
def crear_producto():
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    conn = get_db_connection()
    conn.execute('INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
                 (nombre, categoria, precio, stock))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Mostrar formulario para editar producto
@app.route('/editar/<int:id>', methods=['GET'])
def editar_producto_form(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar_producto.html', producto=producto)

# Procesar edición de producto
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_producto(id):
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    conn = get_db_connection()
    conn.execute('UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id = ?',
                 (nombre, categoria, precio, stock, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Eliminar producto
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)