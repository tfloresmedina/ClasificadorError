from datetime import datetime

from app.database.connection import db


class Ejercicio(db.Model):

    __tablename__ = 'ejercicios'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(200),
        nullable=False
    )

    enunciado = db.Column(
        db.Text,
        nullable=False
    )

    tipo_ejercicio = db.Column(
        db.String(100),
        nullable=False
    )

    competencia = db.Column(
        db.String(150),
        nullable=False
    )

    nivel_dificultad = db.Column(
        db.String(50),
        default='medio'
    )

    puntaje = db.Column(
        db.Float,
        default=1
    )

    respuesta_correcta = db.Column(
        db.Text,
        nullable=True
    )

    procedimiento_modelo = db.Column(
        db.Text,
        nullable=True
    )

    imagen_modelo = db.Column(
        db.String(255),
        nullable=True
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    evaluacion_id = db.Column(
        db.Integer,
        db.ForeignKey('evaluaciones.id'),
        nullable=False
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    respuestas = db.relationship(
        'RespuestaAlumno',
        backref='ejercicio',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):

        return (
            f'<Ejercicio {self.titulo}>'
        )