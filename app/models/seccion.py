from app.database.connection import db


class Seccion(db.Model):

    __tablename__ = 'secciones'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(10),
        nullable=False
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    docente_id = db.Column(

        db.Integer,

        db.ForeignKey(
            'docentes.id'
        ),

        nullable=True
    )
    estudiantes = db.relationship(
        'Estudiante',
        backref='seccion',
        lazy=True
    )

    evaluaciones = db.relationship(
        'Evaluacion',
        backref='seccion',
        lazy=True
    )
    
    def __repr__(self):
        return f'<Seccion {self.nombre}>'