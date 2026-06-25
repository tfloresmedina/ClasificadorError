from app.database.connection import db

from app.models.docente import Docente


class DocenteService:


    @staticmethod
    def listar_docentes():

        return Docente.query.order_by(
            Docente.id.desc()
        ).all()


    @staticmethod
    def obtener_docente(id):

        return Docente.query.get_or_404(id)


    @staticmethod
    def crear_docente(data):

        docente = Docente(

            codigo=data['codigo'],

            nombres=data['nombres'],

            apellidos=data['apellidos'],

            especialidad=data['especialidad']
        )

        db.session.add(docente)

        db.session.commit()

        return docente


    @staticmethod
    def actualizar_docente(docente, data):

        docente.codigo = data['codigo']

        docente.nombres = data['nombres']

        docente.apellidos = data['apellidos']

        docente.especialidad = data['especialidad']

        db.session.commit()

        return docente


    @staticmethod
    def eliminar_docente(docente):

        db.session.delete(docente)

        db.session.commit()