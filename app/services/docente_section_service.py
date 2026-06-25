from flask_login import (
    current_user
)

from app.models.docente import (
    Docente
)

from app.models.seccion import (
    Seccion
)


class DocenteSectionService:


    @staticmethod
    def obtener_secciones_docente():


        # =============================================
        # DOCENTE
        # =============================================

        docente = (

            Docente
            .query
            .filter_by(

                id=current_user.id
            )
            .first()
        )


        if not docente:


            return []


        # =============================================
        # SECCIONES
        # =============================================

        secciones = (

            Seccion
            .query
            .filter_by(

                docente_id=
                    docente.id
            )
            .all()
        )


        return secciones