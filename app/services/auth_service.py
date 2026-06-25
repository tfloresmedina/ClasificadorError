from app.models.usuario import (
    Usuario
)


class AuthService:


    @staticmethod
    def autenticar_usuario(


        username,

        password
    ):


        usuario = (

            Usuario
            .query
            .filter_by(

                username=username
            )
            .first()
        )


        # =============================================
        # VALIDAR USUARIO
        # =============================================

        if not usuario:


            return {

                'success': False,

                'mensaje':
                    'Usuario no encontrado.'
            }


        # =============================================
        # VALIDAR PASSWORD
        # =============================================

        if not usuario.check_password(
            password
        ):


            return {

                'success': False,

                'mensaje':
                    'Contraseña incorrecta.'
            }


        # =============================================
        # VALIDAR ESTADO
        # =============================================

        if not usuario.activo:


            return {

                'success': False,

                'mensaje':
                    'Usuario inactivo.'
            }


        # =============================================
        # LOGIN CORRECTO
        # =============================================

        return {

            'success': True,

            'usuario': usuario
        }