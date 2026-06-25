from datetime import datetime

from app.database.connection import db


class Bimestre(db.Model):


    __tablename__ = 'bimestres'


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

    nombre = db.Column(

        db.String(100),

        nullable=False
    )


    descripcion = db.Column(

        db.Text,

        nullable=True
    )


    estado = db.Column(

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
    # RELACIÓN EVALUACIONES
    # =====================================================

    evaluaciones = db.relationship(

        'Evaluacion',

        backref='bimestre',

        lazy=True,

        cascade='all, delete-orphan'
    )


    # =====================================================
    # REPRESENTACIÓN
    # =====================================================

    def __repr__(self):


        return (

            f'<Bimestre {self.nombre}>'
        )