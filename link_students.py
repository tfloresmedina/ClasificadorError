from app import create_app

from app.database.connection import db

from app.models.usuario import (
    Usuario
)

from app.models.estudiante import (
    Estudiante
)


app = create_app()


with app.app_context():


    estudiantes = (

        Estudiante
        .query
        .all()
    )


    for estudiante in estudiantes:


        # =============================================
        # USERNAME SIMPLE
        # =============================================

        username = (

            estudiante.nombres
            .lower()
            .replace(' ', '')
        )


        # =============================================
        # EXISTE USUARIO
        # =============================================

        usuario = (

            Usuario
            .query
            .filter_by(
                username=username
            )
            .first()
        )


        if not usuario:


            usuario = Usuario(

                nombres=
                    estudiante.nombres,

                email=
                    f'{username}@tamara.com',

                username=
                    username,

                rol='estudiante'
            )


            usuario.set_password(
                '123456'
            )


            db.session.add(
                usuario
            )


            db.session.commit()


        # =============================================
        # VINCULAR
        # =============================================

        estudiante.usuario_id = (
            usuario.id
        )


        db.session.commit()


        print(

            f'Estudiante vinculado: '
            f'{estudiante.nombres}'
        )


    print(

        'Proceso completado.'
    )