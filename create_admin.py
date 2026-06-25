from app import create_app

from app.database.connection import db

from app.models.usuario import (
    Usuario
)


app = create_app()


with app.app_context():


    # =============================================
    # EXISTE
    # =============================================

    existe = (

        Usuario
        .query
        .filter_by(
            username='admin'
        )
        .first()
    )


    if existe:


        print(

            'El administrador ya existe.'
        )


    else:


        admin = Usuario(

            nombres='Administrador TAMARA',

            email='admin@tamara.com',

            username='admin',

            rol='administrador'
        )


        admin.set_password(
            'admin123'
        )


        db.session.add(
            admin
        )


        db.session.commit()


        print(

            'Administrador creado correctamente.'
        )