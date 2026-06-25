from datetime import datetime

from app.database.connection import db


class Estudiante(db.Model):

    __tablename__ = 'estudiantes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    nombres = db.Column(
        db.String(100),
        nullable=False
    )

    apellidos = db.Column(
        db.String(100),
        nullable=False
    )

    fecha_nacimiento = db.Column(
        db.Date,
        nullable=True
    )

    grado_id = db.Column(
        db.Integer,
        db.ForeignKey('grados.id'),
        nullable=False
    )

    seccion_id = db.Column(
        db.Integer,
        db.ForeignKey('secciones.id'),
        nullable=False
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(

        db.Integer,

        db.ForeignKey(
            'usuarios.id'
        ),

        nullable=True
    )


    examenes = db.relationship(
        'ExamenAlumno',
        backref='estudiante',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def nombre_completo(self):
        return (
            f'{self.nombres} {self.apellidos}'
        )

    def __repr__(self):
        return f'<Estudiante {self.codigo}>'