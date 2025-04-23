from flask import Blueprint, render_template

rutas_bp = Blueprint('rutas', __name__)

# Ruta para la página principal
@rutas_bp.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de inicio de sesión
@rutas_bp.route('/login')
def login():
    return render_template('login.html')

# Ruta para la página de registro
@rutas_bp.route('/registro')
def registro():
    return render_template('register.html')


# Ruta para el dashboard del superadministrador
@rutas_bp.route('/superadmin/dashboard')
def superadmin_dashboard():
    return render_template('superadmin/dashboard_superadmin.html')

# @rutas_bp.route('/usuarios')
# def gestion_usuarios():
#     return render_template('superadmin/gestion_usuarios.html')