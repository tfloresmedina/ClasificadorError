from sqlalchemy import func

from app.database.connection import db

from app.models.resultado_analisis import (
    ResultadoAnalisis
)


class TeacherDashboardService:


    @staticmethod
    def obtener_metricas_docente():


        # =============================================
        # TOTAL
        # =============================================

        total_analisis = (

            ResultadoAnalisis
            .query
            .count()
        )


        # =============================================
        # CORRECTOS
        # =============================================

        correctos = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=True
            )
            .count()
        )


        # =============================================
        # INCORRECTOS
        # =============================================

        incorrectos = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=False
            )
            .count()
        )


        # =============================================
        # RIESGO ALTO
        # =============================================

        riesgo_alto = (

            ResultadoAnalisis
            .query
            .filter_by(
                riesgo_academico='alto'
            )
            .count()
        )


        # =============================================
        # OCR PROMEDIO
        # =============================================

        promedio_ocr = (

            db.session.query(

                func.avg(
                    ResultadoAnalisis.nivel_confianza
                )

            ).scalar()
        )


        if promedio_ocr is None:

            promedio_ocr = 0


        # =============================================
        # PORCENTAJE ÉXITO
        # =============================================

        porcentaje_exito = 0


        if total_analisis > 0:

            porcentaje_exito = (

                correctos
                / total_analisis
            ) * 100


        # =============================================
        # RESPUESTA
        # =============================================

        return {

            'total_analisis':
                total_analisis,

            'correctos':
                correctos,

            'incorrectos':
                incorrectos,

            'riesgo_alto':
                riesgo_alto,

            'promedio_ocr':

                round(
                    promedio_ocr,
                    2
                ),

            'porcentaje_exito':

                round(
                    porcentaje_exito,
                    2
                )
        }