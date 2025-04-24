from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '1234567890'

    # Importar los blueprints
    from app.controllers.rutas_controller import rutas_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.superadmin_controller import superadmin_rutas_bp
    from app.controllers.administrador_controller import administrador_bp
    from app.controllers.bibliotecario_controller import bibliotecario_bp

    # Registro de los blueprints
    app.register_blueprint(rutas_bp)  
    app.register_blueprint(auth_bp)   
    app.register_blueprint(superadmin_rutas_bp, url_prefix='/superadmin')  
    app.register_blueprint(administrador_bp, url_prefix='/administrador')  
    app.register_blueprint(bibliotecario_bp)

    return app