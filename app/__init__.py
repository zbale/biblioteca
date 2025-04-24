from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configura la clave secreta
    app.secret_key = '1234567890'

    # Importa los blueprints
    from app.controllers.rutas_controller import rutas_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.superadmin_controller import superadmin_rutas_bp
    from app.controllers.administrador_controller import administrador_bp

    # Registra los blueprints
    app.register_blueprint(rutas_bp)  # General
    app.register_blueprint(auth_bp)  # Autenticación
    app.register_blueprint(superadmin_rutas_bp, url_prefix='/superadmin')  # Todas las rutas del superadmin
    app.register_blueprint(administrador_bp, url_prefix='/administrador')  # Rutas del administrador

    return app