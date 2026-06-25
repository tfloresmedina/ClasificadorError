from datetime import datetime

from app.database.connection import db


class ExamenAlumno(db.Model):

    __tablename__ = 'examenes_alumno'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    estado = db.Column(
        db.String(30),
        default='pendiente'
    )

    observaciones = db.Column(
        db.Text,
        nullable=True
    )

    porcentaje_analisis = db.Column(
        db.Float,
        default=0
    )

    precision_ocr = db.Column(
        db.Float,
        default=0
    )

    ruta_imagen = db.Column(
    db.String(255),
    nullable=True
    )

    texto_ocr = db.Column(
        db.Text,
        nullable=True
    )

    uso_modelo = db.Column(
        db.Boolean,
        default=False
    )

    estado_ocr = db.Column(
        db.String(30),
        default='pendiente'
    )

    fecha_procesamiento = db.Column(
        db.DateTime,
        nullable=True
    )

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey('estudiantes.id'),
        nullable=False
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
        backref='examen_alumno',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):

        return (
            f'<ExamenAlumno {self.id}>'
        )