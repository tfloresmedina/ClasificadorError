from datetime import datetime

from app.database.connection import db


class Docente(db.Model):

    __tablename__ = 'docentes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    nombres = db.Column(
        db.String(100),
        nullable=False
    )

    apellidos = db.Column(
        db.String(100),
        nullable=False
    )

    especialidad = db.Column(
        db.String(100),
        nullable=False,
        default='Matemática'
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
    evaluaciones = db.relationship(
        'Evaluacion',
        backref='docente',
        lazy=True,
        cascade='all, delete-orphan'
    )
 
    secciones = db.relationship(

        'Seccion',

        backref='docente',

        lazy=True
    )

    def nombre_completo(self):

        return (
            f'{self.nombres} {self.apellidos}'
        )

    def __repr__(self):

        return (
            f'<Docente {self.codigo}>'
        )