from sqlalchemy import func

from app.database.connection import db

from app.models.resultado_analisis import (
    ResultadoAnalisis
)


class DashboardService:


    @staticmethod
    def obtener_metricas():


        # =================================================
        # TOTAL ANÁLISIS
        # =================================================

        total_analisis = (

            ResultadoAnalisis
            .query
            .count()
        )


        # =================================================
        # CORRECTOS
        # =================================================

        total_correctos = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=True
            )
            .count()
        )


        # =================================================
        # INCORRECTOS
        # =================================================

        total_incorrectos = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=False
            )
            .count()
        )


        # =================================================
        # PROMEDIO CONFIANZA
        # =================================================

        promedio_confianza = (

            db.session.query(

                func.avg(
                    ResultadoAnalisis.nivel_confianza
                )

            ).scalar()
        )


        if promedio_confianza is None:

            promedio_confianza = 0


        # =================================================
        # ERRORES FRECUENTES
        # =================================================

        errores_frecuentes = (

            db.session.query(

                ResultadoAnalisis.tipo_error,

                func.count(
                    ResultadoAnalisis.id
                )

            )
            .filter(
                ResultadoAnalisis.tipo_error.isnot(None),
                ResultadoAnalisis.tipo_error != ''
            )
            .group_by(
                ResultadoAnalisis.tipo_error
            )
            .order_by(
                func.count(ResultadoAnalisis.id).desc()
            )
            .limit(8)
            .all()
        )

        # =================================================
        # SEVERIDAD ERRORES
        # =================================================

        severidad_errores = (

            db.session.query(

                ResultadoAnalisis.severidad_error,

                func.count(
                    ResultadoAnalisis.id
                )
            )

            .group_by(
                ResultadoAnalisis.severidad_error
            )

            .all()
        )


        # =================================================
        # COMPETENCIAS
        # =================================================

        competencias = (

            db.session.query(

                ResultadoAnalisis.competencia,

                func.count(
                    ResultadoAnalisis.id
                )
            )

            .group_by(
                ResultadoAnalisis.competencia
            )

            .all()
        )


        # =================================================
        # PROCESOS MATEMÁTICOS
        # =================================================

        procesos_matematicos = (

            db.session.query(

                ResultadoAnalisis.fase_polya,

                func.count(
                    ResultadoAnalisis.id
                )
            )

            .group_by(
                ResultadoAnalisis.fase_polya
            )

            .all()
        )


        # =================================================
        # VALIDACIÓN ALGEBRAICA
        # =================================================

        validaciones_correctas = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=True
            )
            .count()
        )


        validaciones_incorrectas = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=False
            )
            .count()
        )

        return {

            'total_errores':
                total_incorrectos,

            'total_estudiantes':
                db.session.query(
                    func.count(
                        func.distinct(
                            ResultadoAnalisis.respuesta_alumno_id
                        )
                    )
                ).scalar() or 0,

            'severidad_errores':
                severidad_errores,

            'competencias':
                competencias,

            'procesos_matematicos':
                procesos_matematicos,

            'validaciones_correctas':
                validaciones_correctas,

            'validaciones_incorrectas':
                validaciones_incorrectas,

            'total_analisis':
                total_analisis,

            'total_correctos':
                total_correctos,

            'total_incorrectos':
                total_incorrectos,
            

            'promedio_confianza':

                round(
                    promedio_confianza,
                    2
                ),

            'errores_frecuentes':
                errores_frecuentes
        }
