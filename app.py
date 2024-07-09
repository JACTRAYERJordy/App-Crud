from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jordy.2003'
app.config['MYSQL_DB'] = 'my_library'

mysql = MySQL(app)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para listar los libros
@app.route('/books')
def list_books():
    # Conexión a la base de datos y obtención de los libros
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    # Renderizar la plantilla list_books.html con los datos obtenidos
    return render_template('list_books.html', books=books)

# Ruta para agregar un nuevo libro
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        print(request.form)
        if 'genre' in request.form:  # Verificar si 'genre' está presente en request.form
            details = request.form
            title = details['title']
            author = details['author']
            year = details['year']
            genre = details['genre']  # Obtener el valor del campo genre del formulario
            stock = details['stock']

            # Insertar los datos del nuevo libro en la base de datos
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO books(title, author, year, genre, stock) VALUES (%s, %s, %s, %s, %s)", (title, author, year, genre, stock))
            mysql.connection.commit()
            cur.close()
            flash('Book added successfully')
            return redirect(url_for('list_books'))
        else:
            flash('Error: Campo "genre" no encontrado en el formulario.')
            return redirect(url_for('add_book'))
    return render_template('add_book.html')

# Ruta para editar un libro existente
@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    # Obtener los datos del libro a editar
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", [id])
    book = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        details = request.form
        title = details['title']
        author = details['author']
        year = details['year']

        # Actualizar los datos del libro en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s", (title, author, year, id))
        mysql.connection.commit()
        cur.close()
        flash('Book updated successfully')
        return redirect(url_for('list_books'))

    # Renderizar la plantilla edit_book.html con los datos del libro
    return render_template('edit_book.html', book=book)

# Ruta para eliminar un libro
@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    # Eliminar el libro de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Book deleted successfully')
    return redirect(url_for('list_books'))

if __name__ == '__main__':
    app.run(debug=True)
