from functools import wraps

from flask import (

    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user
)


def role_required(


    *roles
):


    def decorator(func):


        @wraps(func)
        def wrapper(


            *args,

            **kwargs
        ):


            # =========================================
            # LOGIN
            # =========================================

            if not current_user.is_authenticated:


                flash(

                    'Debe iniciar sesión.',

                    'danger'
                )


                return redirect(

                    url_for(
                        'auth.login'
                    )
                )


            # =========================================
            # ROL
            # =========================================

            if current_user.rol not in roles:


                flash(

                    'No tiene permisos '
                    'para acceder.',

                    'danger'
                )


                return redirect(

                    url_for(
                        'dashboard.dashboard_principal'
                    )
                )


            return func(

                *args,

                **kwargs
            )


        return wrapper


    return decorator