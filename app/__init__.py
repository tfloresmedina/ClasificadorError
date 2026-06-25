from flask import Flask
from flask_migrate import Migrate
from flask_login import (
    LoginManager
)
from app.config import Config

from app.database.connection import db

# MODELOS
from app.models.grado import Grado
from app.models.seccion import Seccion
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.models.evaluacion import Evaluacion
from app.models.ejercicio import Ejercicio
from app.models.examen_alumno import ExamenAlumno
from app.models.bimestre import (
    Bimestre
)
# RUTAS
from app.routes.estudiante_routes import (
    estudiante_bp
)

from app.routes.docente_routes import (
    docente_bp
)

from app.routes.auth_routes import (
    auth_bp
)

from app.models.respuesta_alumno import (
    RespuestaAlumno
)

from app.models.resultado_analisis import (
    ResultadoAnalisis
)

from app.models.usuario import (
    Usuario
)

from app.routes.resultados_routes import (
    resultados_bp
)

from app.routes.dashboard_routes import (
    dashboard_bp
)

from app.routes.seccion_routes import (
    seccion_bp
)

from app.routes.evaluacion_routes import (
    evaluacion_bp
)

from app.routes.reportes_routes import (
    resultados_bp as reportes_bp
)

migrate = Migrate()

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)


    # =====================================================
    # LOGIN MANAGER
    # =====================================================

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    # BLUEPRINTS
   
    app.register_blueprint(
        auth_bp
    )

    app.register_blueprint(
        estudiante_bp
    )

    app.register_blueprint(
        docente_bp
    )
    
    app.register_blueprint(
    resultados_bp
    )

    app.register_blueprint(
    dashboard_bp
    )
    
    app.register_blueprint(
    seccion_bp
    )

    app.register_blueprint(
    evaluacion_bp
    )

    app.register_blueprint(
    reportes_bp
    )
    
        # =====================================================
    # USER LOADER
    # =====================================================

    @login_manager.user_loader
    def load_user(user_id):


        return Usuario.query.get(
            int(user_id)
        )
    
    return app