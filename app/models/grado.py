from app.database.connection import db


class Grado(db.Model):

    __tablename__ = 'grados'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    estudiantes = db.relationship(
        'Estudiante',
        backref='grado',
        lazy=True
    )
    
    evaluaciones = db.relationship(
        'Evaluacion',
        backref='grado',
        lazy=True
    )
    def __repr__(self):
        return f'<Grado {self.nombre}>'