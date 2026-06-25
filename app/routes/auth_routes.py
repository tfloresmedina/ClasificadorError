from flask import (

    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (

    login_user,
    logout_user,
    login_required,
    current_user
)

from app.services.auth_service import (
    AuthService
)


auth_bp = Blueprint(

    'auth',

    __name__
)


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route(
    '/login',
    methods=['GET', 'POST']
)

def login():


    # =============================================
    # YA AUTENTICADO
    # =============================================

    if current_user.is_authenticated:


        return redirect(

            url_for(
                'dashboard.dashboard_principal'
            )
        )


    # =============================================
    # POST
    # =============================================

    if request.method == 'POST':


        username = request.form.get(
            'username'
        )


        password = request.form.get(
            'password'
        )


        resultado = (

            AuthService
            .autenticar_usuario(

                username=
                    username,

                password=
                    password
            )
        )


        # =============================================
        # LOGIN OK
        # =============================================

        if resultado.get(
            'success'
        ):


            usuario = resultado.get(
                'usuario'
            )


            login_user(
                usuario
            )


            flash(

                'Bienvenido al sistema.',

                'success'
            )


            return redirect(

                url_for(
                    'dashboard.dashboard_principal'
                )
            )


        # =============================================
        # ERROR
        # =============================================

        flash(

            resultado.get(
                'mensaje'
            ),

            'danger'
        )


    return render_template(

        'auth/login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route(
    '/logout'
)

@login_required
def logout():


    logout_user()


    flash(

        'Sesión cerrada correctamente.',

        'info'
    )


    return redirect(

        url_for(
            'auth.login'
        )
    )