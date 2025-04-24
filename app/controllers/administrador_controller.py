from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
import mysql.connector

# Blueprint para el Administrador
administrador_bp = Blueprint('administrador', __name__, url_prefix='/administrador')

@administrador_bp.route('/dashboard')
def administrador_dashboard():
    return render_template('administrador/dashboard_administrador.html')

@administrador_bp.route('/usuarios', methods=['GET', 'POST'])
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

            # Limitar los roles que puede asignar el Administrador
            if rol_id not in ['3', '4']:  # Solo puede asignar Bibliotecarios (3) y Estudiantes (4)
                flash('No tienes permiso para asignar este rol.', 'danger')
                return redirect(url_for('administrador.gestion_usuarios'))

            if not password:
                flash('La contraseña es obligatoria.', 'danger')
                return redirect(url_for('administrador.gestion_usuarios'))

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
        cursor.execute("SELECT id_usuario, nombre, email, rol_id FROM usuarios WHERE rol_id IN (3, 4)")
        usuarios = cursor.fetchall()

    except mysql.connector.Error as db_err:
        flash(f'Error de conexión a la base de datos: {db_err}', 'danger')
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    # Cambiar el nombre de la plantilla aquí
    return render_template('administrador/gestionar_usuarios.html', usuarios=usuarios)

@administrador_bp.route('/usuarios/eliminar/<int:id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor()

        # Eliminar el usuario con el ID proporcionado
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s AND rol_id IN (3, 4)", (id_usuario,))
        conn.commit()

        flash('Usuario eliminado exitosamente.', 'success')
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f'Ocurrió un error al eliminar el usuario: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('administrador.gestion_usuarios'))

@administrador_bp.route('/usuarios/editar', methods=['POST'])
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

    return redirect(url_for('administrador.gestion_usuarios'))

@administrador_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        nueva_contraseña = request.form.get('password')

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='valecita',
                database='biblioteca_db'
            )
            cursor = conn.cursor()

            if nueva_contraseña:
                contraseña_encriptada = generate_password_hash(nueva_contraseña)
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s, contraseña = %s
                    WHERE rol_id = 2
                """, (nombre, email, contraseña_encriptada))
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s
                    WHERE rol_id = 2
                """, (nombre, email))

            conn.commit()
            flash('Perfil actualizado exitosamente.', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f'Ocurrió un error al actualizar el perfil: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('administrador.perfil'))

    # Obtener los datos actuales del Administrador
    administrador = {}
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nombre, email FROM usuarios WHERE rol_id = 2 LIMIT 1")
        administrador = cursor.fetchone()
    except mysql.connector.Error as e:
        flash(f'Ocurrió un error al cargar el perfil: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('administrador/perfil_administrador.html', administrador=administrador)

@administrador_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if request.method == 'POST':
        # Procesar los cambios en la configuración
        horario = request.form.get('horario')
        max_prestamos = request.form.get('max_prestamos')

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='valecita',
                database='biblioteca_db'
            )
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE configuracion
                SET horario = %s, max_prestamos = %s
                WHERE id = 1
            """, (horario, max_prestamos))
            conn.commit()
            flash('Configuración actualizada exitosamente.', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f'Ocurrió un error al actualizar la configuración: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

    # Obtener la configuración actual
    configuracion = {}
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT horario, max_prestamos FROM configuracion WHERE id = 1")
        configuracion = cursor.fetchone()
    except mysql.connector.Error as e:
        flash(f'Ocurrió un error al cargar la configuración: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('administrador/configuracion.html', configuracion=configuracion)