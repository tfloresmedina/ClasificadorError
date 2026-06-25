from flask_login import (
    current_user
)

from app.models.resultado_analisis import (
    ResultadoAnalisis
)

from app.models.respuesta_alumno import (
    RespuestaAlumno
)

from app.models.examen_alumno import (
    ExamenAlumno
)

from app.models.estudiante import (
    Estudiante
)


class StudentResultService:


    @staticmethod
    def obtener_resultados_estudiante():


        # =============================================
        # VALIDAR ESTUDIANTE
        # =============================================

        estudiante = (

            Estudiante
            .query
            .filter_by(

                usuario_id=
                    current_user.id
            )
            .first()
        )


        if not estudiante:


            return []


        # =============================================
        # RESULTADOS
        # =============================================

        resultados = (

            ResultadoAnalisis
            .query
            .join(

                RespuestaAlumno,

                ResultadoAnalisis
                .respuesta_alumno_id
                == RespuestaAlumno.id
            )
            .join(

                ExamenAlumno,

                RespuestaAlumno
                .examen_alumno_id
                == ExamenAlumno.id
            )
            .filter(

                ExamenAlumno.estudiante_id
                == estudiante.id
            )
            .order_by(

                ResultadoAnalisis
                .fecha_registro
                .desc()
            )
            .all()
        )


        return resultados