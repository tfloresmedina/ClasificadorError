from datetime import datetime

from werkzeug.security import (

    generate_password_hash,
    check_password_hash
)

from app.database.connection import db

from flask_login import UserMixin

class Usuario(

    UserMixin,

    db.Model
):

    __tablename__ = 'usuarios'

    # =====================================================
    # ID
    # =====================================================

    id = db.Column(

        db.Integer,

        primary_key=True
    )


    # =====================================================
    # INFORMACIÓN
    # =====================================================

    nombres = db.Column(

        db.String(150),

        nullable=False
    )


    email = db.Column(

        db.String(150),

        unique=True,

        nullable=False
    )


    username = db.Column(

        db.String(100),

        unique=True,

        nullable=False
    )


    password_hash = db.Column(

        db.String(255),

        nullable=False
    )


    # =====================================================
    # ROL
    # =====================================================

    rol = db.Column(

        db.String(50),

        nullable=False,

        default='docente'
    )


    # =====================================================
    # ESTADO
    # =====================================================

    activo = db.Column(

        db.Boolean,

        default=True
    )


    # =====================================================
    # FECHA
    # =====================================================

    fecha_registro = db.Column(

        db.DateTime,

        default=datetime.utcnow
    )


    # =====================================================
    # PASSWORD
    # =====================================================

    def set_password(


        self,

        password
    ):


        self.password_hash = (

            generate_password_hash(
                password
            )
        )


    def check_password(


        self,

        password
    ):


        return check_password_hash(

            self.password_hash,

            password
        )
    # =====================================================
    # RELACIÓN ESTUDIANTE
    # =====================================================

    estudiante = db.relationship(

        'Estudiante',

        backref='usuario',

        uselist=False
    )

    # =====================================================
    # REPRESENTACIÓN
    # =====================================================

    def __repr__(self):


        return (

            f'<Usuario {self.username}>'
        )