from flask_login import (
    current_user
)


class RoleService:


    @staticmethod
    def es_admin():


        return (

            current_user.is_authenticated

            and

            current_user.rol
            == 'administrador'
        )


    @staticmethod
    def es_docente():


        return (

            current_user.is_authenticated

            and

            current_user.rol
            == 'docente'
        )


    @staticmethod
    def es_estudiante():


        return (

            current_user.is_authenticated

            and

            current_user.rol
            == 'estudiante'
        )


    @staticmethod
    def es_padre():


        return (

            current_user.is_authenticated

            and

            current_user.rol
            == 'padre'
        )