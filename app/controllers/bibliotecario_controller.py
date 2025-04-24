from flask import Blueprint, render_template, request, redirect, flash, url_for
import mysql.connector

bibliotecario_bp = Blueprint('bibliotecario', __name__, url_prefix='/bibliotecario')

@bibliotecario_bp.route('/catalogo', methods=['GET'])
def catalogo():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)

        # Obtener todos los libros de la base de datos
        cursor.execute("""
            SELECT libros.id_libro, libros.titulo, libros.isbn, categorias.nombre_categoria AS categoria, libros.fecha_publicacion
            FROM libros
            LEFT JOIN categorias ON libros.categoria_id = categorias.id_categoria
        """)
        libros = cursor.fetchall()
    except mysql.connector.Error as e:
        flash(f'Error al cargar el catálogo: {e}', 'danger')
        libros = []
    finally:
        cursor.close()
        conn.close()

    # Pasar la lista de libros a la plantilla
    return render_template('bibliotecario/catalogo.html', libros=libros)

@bibliotecario_bp.route('/prestamos', methods=['GET', 'POST'])
def prestamos():
    if request.method == 'POST':
        # Lógica para registrar un préstamo
        flash('Préstamo registrado exitosamente.', 'success')
        return redirect(url_for('bibliotecario.prestamos'))
    # Aquí iría la lógica para obtener los préstamos actuales
    prestamos = [
        {"id": 1, "usuario": "Juan Pérez", "libro": "El Quijote", "fecha_prestamo": "2025-04-01", "devuelto": False},
    ]
    return render_template('bibliotecario/prestamos.html', prestamos=prestamos)

@bibliotecario_bp.route('/devoluciones', methods=['GET', 'POST'])
def devoluciones():
    if request.method == 'POST':
        # Lógica para registrar una devolución
        flash('Devolución registrada exitosamente.', 'success')
        return redirect(url_for('bibliotecario.devoluciones'))
    # Aquí iría la lógica para obtener las devoluciones pendientes
    devoluciones = [
        {"id": 1, "usuario": "Juan Pérez", "libro": "El Quijote", "fecha_prestamo": "2025-04-01", "devuelto": False},
    ]
    return render_template('bibliotecario/devoluciones.html', devoluciones=devoluciones)

@bibliotecario_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('bibliotecario/dashboard_bibliotecario.html')

@bibliotecario_bp.route('/agregar_libro', methods=['GET', 'POST'])
def agregar_libro():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            titulo = request.form.get('titulo')
            autor = request.form.get('autor')
            isbn = request.form.get('isbn')
            categoria_id = request.form.get('categoria_id')
            fecha_publicacion = request.form.get('fecha_publicacion')

            # Verificar que todos los campos estén completos
            if not titulo or not autor or not isbn or not categoria_id or not fecha_publicacion:
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('bibliotecario.agregar_libro'))

            # Verificar unicidad del ISBN
            cursor.execute("SELECT * FROM libros WHERE isbn = %s", (isbn,))
            if cursor.fetchone():
                flash('El ISBN ya está registrado. Por favor, usa uno diferente.', 'danger')
                return redirect(url_for('bibliotecario.agregar_libro'))

            # Insertar el libro en la tabla `libros`
            cursor.execute("""
                INSERT INTO libros (titulo, isbn, categoria_id, fecha_publicacion)
                VALUES (%s, %s, %s, %s)
            """, (titulo, isbn, categoria_id, fecha_publicacion))
            conn.commit()

            # Obtener el ID del libro recién insertado
            id_libro = cursor.lastrowid

            # Verificar si el autor ya existe
            cursor.execute("SELECT id_autor FROM autores WHERE nombre = %s", (autor,))
            autor_result = cursor.fetchone()
            if autor_result:
                id_autor = autor_result['id_autor']
            else:
                # Insertar el autor en la tabla `autores`
                cursor.execute("INSERT INTO autores (nombre) VALUES (%s)", (autor,))
                conn.commit()
                id_autor = cursor.lastrowid

            # Insertar la relación en la tabla `libro_autor`
            cursor.execute("""
                INSERT INTO libro_autor (id_libro, id_autor)
                VALUES (%s, %s)
            """, (id_libro, id_autor))
            conn.commit()

            flash('Libro registrado exitosamente.', 'success')
            return redirect(url_for('bibliotecario.agregar_libro'))  # Permanecer en la misma página

        # Obtener las categorías para el formulario
        cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias")
        categorias = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f'Ocurrió un error al registrar el libro: {e}', 'danger')
        categorias = []
    finally:
        cursor.close()
        conn.close()

    return render_template('bibliotecario/agregar_libro.html', categorias=categorias)

@bibliotecario_bp.route('/procesar_prestamo', methods=['GET', 'POST'])
def procesar_prestamo():
    if request.method == 'POST':
        id_estudiante = request.form.get('id_estudiante')
        codigo_libro = request.form.get('codigo_libro')

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='valecita',
                database='biblioteca_db'
            )
            cursor = conn.cursor()

            # Validar morosidad del estudiante
            cursor.execute("""
                SELECT COUNT(*) FROM prestamos
                WHERE id_estudiante = %s AND devuelto = 0
            """, (id_estudiante,))
            morosidad = cursor.fetchone()[0]
            if morosidad >= 3:
                flash('El estudiante tiene más de 3 libros atrasados. No se puede procesar el préstamo.', 'danger')
                return redirect(url_for('bibliotecario.procesar_prestamo'))

            # Registrar el préstamo
            cursor.execute("""
                INSERT INTO prestamos (id_estudiante, codigo_libro, fecha_prestamo, fecha_devolucion, devuelto)
                VALUES (%s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 15 DAY), 0)
            """, (id_estudiante, codigo_libro))
            conn.commit()
            flash('Préstamo registrado exitosamente.', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f'Ocurrió un error al procesar el préstamo: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('bibliotecario.prestamos'))

    return render_template('bibliotecario/procesar_prestamo.html')

@bibliotecario_bp.route('/eliminar_libro/<int:id_libro>', methods=['POST'])
def eliminar_libro(id_libro):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id_libro = %s", (id_libro,))
        conn.commit()
        flash('Libro eliminado exitosamente.', 'success')
    except mysql.connector.Error as e:
        flash(f'Error al eliminar el libro: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('bibliotecario.catalogo'))

@bibliotecario_bp.route('/editar_libro/<int:id_libro>', methods=['POST'])
def editar_libro(id_libro):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor()

        # Obtener los datos del formulario
        titulo = request.form.get('titulo')
        isbn = request.form.get('isbn')
        categoria_id = request.form.get('categoria_id')
        fecha_publicacion = request.form.get('fecha_publicacion')

        # Actualizar el libro en la base de datos
        cursor.execute("""
            UPDATE libros
            SET titulo = %s, isbn = %s, categoria_id = %s, fecha_publicacion = %s
            WHERE id_libro = %s
        """, (titulo, isbn, categoria_id, fecha_publicacion, id_libro))
        conn.commit()
        flash('Libro actualizado exitosamente.', 'success')
    except mysql.connector.Error as e:
        flash(f'Error al actualizar el libro: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('bibliotecario.catalogo'))