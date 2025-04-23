from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import mysql.connector

auth_bp = Blueprint('auth', __name__)

# Ruta para manejar el inicio de sesión
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    datos = request.get_json()
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='valecita',
        database='biblioteca_db'
    )
    cursor = conn.cursor(dictionary=True)

    # Verificar si el usuario existe
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (correo,))
    usuario = cursor.fetchone()

    if usuario and check_password_hash(usuario['contraseña'], contraseña):
        # Retornar el rol del usuario
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario['id_usuario'],
                "nombre": usuario['nombre'],
                "rol": usuario['rol_id']
            }
        }), 200
    else:
        return jsonify({"mensaje": "Correo o contraseña incorrectos"}), 401

    cursor.close()
    conn.close()