from werkzeug.security import generate_password_hash
import mysql.connector

# Datos del superadministrador
nombre = 'superadmin'
email = 'adminvalecita@gmail.com'
contraseña_plana = '1234' 
rol_superadmin = 'Superadmin' 

# Encriptar la contraseña
contraseña_encriptada = generate_password_hash(contraseña_plana)

# Conexión a tu base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='valecita',
    database='biblioteca_db'
)
cursor = conn.cursor()

# Obtener el id_rol del superadmin
cursor.execute("SELECT id_rol FROM roles WHERE nombre_rol = %s", (rol_superadmin,))
resultado = cursor.fetchone()

if resultado:
    id_rol = resultado[0]

    # Insertar el superadmin
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, contraseña, rol_id)
        VALUES (%s, %s, %s, %s)
    """, (nombre, email, contraseña_encriptada, id_rol))

    conn.commit()
    print("Superadministrador creado exitosamente.")
else:
    print("El rol 'Superadmin' no existe. Asegúrate de haberlo insertado en la tabla roles.")

cursor.close()
conn.close()
