from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agends_app'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (nombre, apellido, telefono, email, descripcion) VALUES (%s,%s,%s,%s,%s)',
        (nombre, apellido, telefono, email, descripcion))
        mysql.connection.commit()
        flash('Contacto Agregado Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/nosotros')
def about():
    return render_template('nosotros.html')

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts 
            SET nombre = %s,
                apellido = %s,
                telefono = %s,
                email = %s,
                descripcion = %s
            WHERE id = %s
            """, (nombre, apellido, telefono, email, descripcion, id))
        mysql.connection.commit()
        flash('Contacto Actualizado Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado Satisfactoriamente')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run( port = 3000, debug = True)