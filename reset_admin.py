from app import create_app
from app.database.connection import db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(
        username='admin'
    ).first()

    if usuario:

        usuario.set_password('admin')

        db.session.commit()

        print('Contraseña actualizada')

    else:

        admin = Usuario(
            nombres='Administrador',
            email='admin@tamara.com',
            username='admin',
            rol='administrador',
            activo=True
        )

        admin.set_password('admin')

        db.session.add(admin)
        db.session.commit()

        print('Usuario admin creado')