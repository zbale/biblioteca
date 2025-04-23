from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
import mysql.connector

# Blueprints
superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')
superadmin_rutas_bp = Blueprint('superadmin_rutas', __name__)


@superadmin_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        nueva_contraseña = request.form.get('password')

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='valecita',
            database='biblioteca_db'
        )
        cursor = conn.cursor()

        try:
            if nueva_contraseña:
                contraseña_encriptada = generate_password_hash(nueva_contraseña)
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s, contraseña = %s
                    WHERE rol_id = 1
                """, (nombre, email, contraseña_encriptada))
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, email = %s
                    WHERE rol_id = 1
                """, (nombre, email))

            conn.commit()
            flash('Perfil actualizado exitosamente.' if cursor.rowcount > 0 else 'No se encontraron cambios.', 'success' if cursor.rowcount > 0 else 'warning')

        except Exception as e:
            conn.rollback()
            flash(f'Ocurrió un error al actualizar el perfil: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('superadmin_rutas.superadmin_dashboard'))

    # Cargar datos actuales
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='valecita',
        database='biblioteca_db'
    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT nombre, email FROM usuarios WHERE rol_id = 1")
        superadmin = cursor.fetchone()
    except Exception as e:
        flash(f'Ocurrió un error al cargar los datos: {e}', 'danger')
        superadmin = {}
    finally:
        cursor.close()
        conn.close()

    return render_template('superadmin/perfil_superadmin.html', superadmin=superadmin)

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


# ========================= GESTIÓN DE USUARIOS =========================
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


# ========================= ELIMINAR USUARIO =========================
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
