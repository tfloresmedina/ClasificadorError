from flask import (

    Blueprint,
    render_template
)

from app.services.dashboard_service import (
    DashboardService
)

from app.services.teacher_dashboard_service import (
    TeacherDashboardService
)

from flask_login import (
    login_required
)

from app.services.role_required_service import (
    role_required
)

from app.services.student_dashboard_service import (
    StudentDashboardService
)

from app.models.seccion import (
    Seccion
)

dashboard_bp = Blueprint(

    'dashboard',

    __name__,

    url_prefix='/dashboard'
)


# =========================================================
# DASHBOARD PRINCIPAL
# =========================================================

@dashboard_bp.route('/')

@login_required
def dashboard_principal():


    metricas = (

        DashboardService
        .obtener_metricas()
    )


    return render_template(

        'dashboard/dashboard.html',

        metricas=
            metricas
    )
# =========================================================
# DASHBOARD DOCENTE
# =========================================================

@dashboard_bp.route('/docente')

@login_required

@role_required(
    'administrador',
    'docente'
)
def dashboard_docente():


    metricas = (

        TeacherDashboardService
        .obtener_metricas_docente()
    )


    return render_template(

        'dashboard/docente.html',

        metricas=
            metricas
    )

# =========================================================
# DASHBOARD ESTUDIANTE
# =========================================================

@dashboard_bp.route(
    '/estudiante',
    methods=['GET']
)

@login_required

@role_required(
    'administrador',
    'estudiante'
)
def dashboard_estudiante():


    metricas = (

        StudentDashboardService
        .obtener_metricas_estudiante()
    )


    return render_template(

        'estudiantes/estudiante.html',

        metricas=
            metricas
    )

