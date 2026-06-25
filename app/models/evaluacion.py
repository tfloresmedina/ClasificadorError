from datetime import datetime

from app.database.connection import db


class Evaluacion(db.Model):

    __tablename__ = 'evaluaciones'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(200),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    unidad = db.Column(
        db.Integer,
        nullable=False
    )

    fecha_evaluacion = db.Column(
        db.Date,
        nullable=False
    )

    estado = db.Column(
        db.String(30),
        default='pendiente'
    )

    observaciones = db.Column(
        db.Text,
        nullable=True
    )

    docente_id = db.Column(
        db.Integer,
        db.ForeignKey('docentes.id'),
        nullable=False
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

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    respuesta_modelo = db.Column(
    db.Text,
    nullable=True
    )

    ruta_modelo = db.Column(
        db.String(255),
        nullable=True
    )
    
    ejercicios = db.relationship(
        'Ejercicio',
        backref='evaluacion',
        lazy=True,
        cascade='all, delete-orphan'
    )

    procedimiento_modelo = db.Column(
        db.Text,
        nullable=True
    )

    def __repr__(self):

        return (
            f'<Evaluacion {self.titulo}>'
        )
    
        # =====================================================
    # BIMESTRE
    # =====================================================

    bimestre_id = db.Column(

        db.Integer,

        db.ForeignKey(
            'bimestres.id'
        ),

        nullable=True
    )


    # =====================================================
    # TIPO EVALUACIÓN
    # =====================================================

    tipo_evaluacion = db.Column(

        db.String(30),

        nullable=False,

        default='unidad'
    )


    # =====================================================
    # COMPETENCIA
    # =====================================================

    competencia = db.Column(

        db.String(255),

        nullable=True
    )

        # =====================================================
    # EXAMEN MODELO
    # =====================================================

    examen_modelo = db.Column(

        db.String(255),

        nullable=True
    )


    modelo_ocr = db.Column(

        db.Text,

        nullable=True
    )


    modelo_normalizado = db.Column(

        db.Text,

        nullable=True
    )