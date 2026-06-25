from app.database.connection import db

from app.models.estudiante import Estudiante


class EstudianteService:


    @staticmethod
    def listar_estudiantes():

        return Estudiante.query.order_by(
            Estudiante.apellidos.asc()
        ).all()


    @staticmethod
    def obtener_estudiante(estudiante_id):

        return Estudiante.query.get_or_404(
            estudiante_id
        )


    @staticmethod
    def crear_estudiante(data):

        existe_codigo = (
            Estudiante.query.filter_by(
                codigo=data['codigo']
            ).first()
        )

        if existe_codigo:

            raise ValueError(
                'El código del estudiante ya existe.'
            )

        estudiante = Estudiante(

            codigo=data['codigo'],

            nombres=data['nombres'],

            apellidos=data['apellidos'],

            fecha_nacimiento=data.get(
                'fecha_nacimiento'
            ),

            grado_id=data['grado_id'],

            seccion_id=data['seccion_id'],

            estado=True
        )

        db.session.add(estudiante)

        db.session.commit()

        return estudiante


    @staticmethod
    def actualizar_estudiante(
        estudiante,
        data
    ):

        estudiante.codigo = data['codigo']

        estudiante.nombres = data['nombres']

        estudiante.apellidos = data['apellidos']

        estudiante.fecha_nacimiento = (
            data.get('fecha_nacimiento')
        )

        estudiante.grado_id = data['grado_id']

        estudiante.seccion_id = data['seccion_id']

        db.session.commit()

        return estudiante


    @staticmethod
    def eliminar_estudiante(estudiante):

        db.session.delete(estudiante)

        db.session.commit()
    