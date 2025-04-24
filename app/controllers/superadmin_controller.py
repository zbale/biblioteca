from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
import mysql.connector

# Blueprints
superadmin_rutas_bp = Blueprint('superadmin_rutas', __name__)


@superadmin_rutas_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='valecita',
                database='biblioteca_db'
            )
            cursor = conn.cursor()

            # Actualizar los datos del perfil
            if password:
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s, contraseña = %s
                    WHERE rol_id = 1
                """, (nombre, email, hashed_password))
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s
                    WHERE rol_id = 1
                """, (nombre, email))

            conn.commit()
            return redirect(url_for('superadmin_rutas.perfil'))
        except mysql.connector.Error as e:
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('superadmin_rutas.perfil'))

    # Obtener los datos actuales del perfil
    superadmin = {}
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE rol_id = 1")
        superadmin = cursor.fetchone()
    except mysql.connector.Error as e:
        flash(f'Ocurrió un error al cargar los datos del perfil: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('superadmin/perfil_super_administrador.html', superadmin=superadmin)

@superadmin_rutas_bp.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='valecita',
                database='biblioteca_db'
            )
            cursor = conn.cursor()

            # Actualizar los datos del perfil
            if password:
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s, contraseña = %s
                    WHERE rol_id = 1
                """, (nombre, email, hashed_password))
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s
                    WHERE rol_id = 1
                """, (nombre, email))

            conn.commit()
            flash('Perfil actualizado exitosamente.', 'success')
            return redirect(url_for('superadmin_rutas.perfil'))
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f'Ocurrió un error al actualizar el perfil: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('superadmin_rutas.perfil'))

    # Obtener los datos actuales del perfil
    superadmin = {}
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE rol_id = 1")
        superadmin = cursor.fetchone()
    except mysql.connector.Error as e:
        flash(f'Ocurrió un error al cargar los datos del perfil: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('superadmin/editar_perfil.html', superadmin=superadmin)

@superadmin_rutas_bp.route('/dashboard')
def superadmin_dashboard():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='valecita',
        database='biblioteca_db'
    )
    cursor = conn.cursor(dictionary=True)

    try:
        # Ejecuta la consulta y consume los resultados
        cursor.execute("SELECT email FROM usuarios WHERE rol_id = 1")
        superadmin = cursor.fetchone()  # Obtiene el primer resultado
        cursor.fetchall()  # Descarta cualquier resultado adicional
    except Exception as e:
        flash(f'Ocurrió un error al cargar el dashboard: {e}', 'danger')
        superadmin = None
    finally:
        cursor.close()
        conn.close()

    return render_template('superadmin/dashboard_superadmin.html', superadmin=superadmin)


@superadmin_rutas_bp.route('/usuarios', methods=['GET', 'POST'])
def gestion_usuarios():
    usuarios = []

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)

        # Procesar formulario si es POST
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            email = request.form.get('email')
            password = request.form.get('password')
            rol_id = request.form.get('rol_id')

            if not password:
                flash('La contraseña es obligatoria.', 'danger')
                return redirect(url_for('superadmin_rutas.gestion_usuarios'))

            contraseña_encriptada = generate_password_hash(password)

            try:
                cursor.execute("""
                    INSERT INTO usuarios (nombre, email, contraseña, rol_id)
                    VALUES (%s, %s, %s, %s)
                """, (nombre, email, contraseña_encriptada, rol_id))
                conn.commit()
                flash('Usuario añadido exitosamente.', 'success')
            except Exception as e:
                conn.rollback()
                flash(f'Ocurrió un error al añadir el usuario: {e}', 'danger')

        # Consultar todos los usuarios después del POST o si es GET
        cursor.execute("SELECT id_usuario, nombre, email, rol_id FROM usuarios")
        usuarios = cursor.fetchall()

    except mysql.connector.Error as db_err:
        flash(f'Error de conexión a la base de datos: {db_err}', 'danger')
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    return render_template('superadmin/gestion_usuarios.html', usuarios=usuarios)

@superadmin_rutas_bp.route('/usuarios/eliminar/<int:id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='valecita',
        database='biblioteca_db'
    )
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        flash('Usuario eliminado exitosamente.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ocurrió un error al eliminar el usuario: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('superadmin_rutas.gestion_usuarios'))

@superadmin_rutas_bp.route('/usuarios/editar', methods=['POST'])
def editar_usuario():
    id_usuario = request.form.get('id_usuario')
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    rol_id = request.form.get('rol_id')

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor()

        # Actualizar los datos del usuario en la base de datos
        cursor.execute("""
            UPDATE usuarios
            SET nombre = %s, email = %s, rol_id = %s
            WHERE id_usuario = %s
        """, (nombre, email, rol_id, id_usuario))
        conn.commit()

        flash('Usuario actualizado exitosamente.', 'success')
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f'Ocurrió un error al actualizar el usuario: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('superadmin_rutas.gestion_usuarios'))
