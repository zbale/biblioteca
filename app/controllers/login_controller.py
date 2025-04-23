from werkzeug.security import check_password_hash
from flask import request, jsonify, session
from app.models.conexion import obtener_conexion  # Ajusta según tu estructura

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    contraseña = data.get('contraseña')

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.*, r.nombre_rol
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id_rol
        WHERE u.email = %s
    """, (correo,))
    usuario = cursor.fetchone()

    if usuario and check_password_hash(usuario['contraseña'], contraseña):
        session['usuario_id'] = usuario['id_usuario']
        session['rol'] = usuario['nombre_rol']
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'usuario': {
                'nombre': usuario['nombre'],
                'rol': usuario['nombre_rol']
            }
        })
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401
