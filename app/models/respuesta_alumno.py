from datetime import datetime

from app.database.connection import db


class RespuestaAlumno(db.Model):

    __tablename__ = 'respuestas_alumno'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    imagen_respuesta = db.Column(
        db.String(255),
        nullable=False
    )

    texto_ocr = db.Column(
        db.Text,
        nullable=True
    )

    expresion_detectada = db.Column(
        db.Text,
        nullable=True
    )

    expresion_normalizada = db.Column(
        db.Text,
        nullable=True
    )

    estado_ocr = db.Column(
        db.String(30),
        default='pendiente'
    )

    precision_ocr = db.Column(
        db.Float,
        default=0
    )

    observaciones_ocr = db.Column(
        db.Text,
        nullable=True
    )

    ejercicio_id = db.Column(
        db.Integer,
        db.ForeignKey('ejercicios.id'),
        nullable=True
    )

    examen_alumno_id = db.Column(
        db.Integer,
        db.ForeignKey('examenes_alumno.id'),
        nullable=False
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    resultado = db.relationship(
        'ResultadoAnalisis',
        backref='respuesta_alumno',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):

        return (
            f'<RespuestaAlumno {self.id}>'
        )