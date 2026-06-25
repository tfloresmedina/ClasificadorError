from app.services.performance_metrics_service import (
    PerformanceMetricsService
)

from app.services.error_frequency_service import (
    ErrorFrequencyService
)

from app.services.student_performance_service import (
    StudentPerformanceService
)

from app.services.classroom_analytics_service import (
    ClassroomAnalyticsService
)

from app.services.risk_detection_service import (
    RiskDetectionService
)

from app.services.learning_trend_service import (
    LearningTrendService
)

from app.services.pedagogical_alert_service import (
    PedagogicalAlertService
)

from app.services.mathematical_profile_service import (
    MathematicalProfileService
)

from app.services.reinforcement_planning_service import (
    ReinforcementPlanningService
)

from app.services.report_summary_service import (
    ReportSummaryService
)

from app.services.dashboard_data_service import (
    DashboardDataService
)

from app.services.result_consolidation_service import (
    ResultConsolidationService
)


class MasterAnalysisService:


    @staticmethod
    def ejecutar_analisis_completo(


        estudiante,

        resultados,

        historico=None
    ):


        if historico is None:

            historico = []


        # MÉTRICAS GENERALES

        metricas = (

            PerformanceMetricsService
            .calcular_metricas(

                resultados
            )
        )


        # FRECUENCIA DE ERRORES

        errores = (

            ErrorFrequencyService
            .calcular_frecuencia(

                resultados
            )
        )


        # RESUMEN DEL ESTUDIANTE

        resumen_estudiante = (

            StudentPerformanceService
            .resumir_desempeno(

                estudiante,

                resultados
            )
        )


        # RIESGO

        riesgo = (

            RiskDetectionService
            .detectar_riesgo(

                resumen_estudiante[
                    'porcentaje_acierto'
                ]
            )
        )


        # TENDENCIA

        tendencia = (

            LearningTrendService
            .analizar_tendencia(

                historico
            )
        )


        # ALERTAS

        alertas = (

            PedagogicalAlertService
            .generar_alertas(

                riesgo,

                tendencia
            )
        )


        # PERFIL MATEMÁTICO

        perfil = (

            MathematicalProfileService
            .construir_perfil(

                porcentaje_acierto=

                    resumen_estudiante[
                        'porcentaje_acierto'
                    ],

                errores_frecuentes=
                    errores,

                dificultad_promedio=
                    'media'
            )
        )


        # PLAN DE REFUERZO

        plan_refuerzo = (

            ReinforcementPlanningService
            .generar_plan(

                debilidad=

                    perfil[
                        'debilidad'
                    ],

                riesgo=
                    riesgo
            )
        )


        # RESUMEN GENERAL

        resumen = (

            ReportSummaryService
            .generar_resumen(

                estudiante=
                    estudiante,

                porcentaje=

                    resumen_estudiante[
                        'porcentaje_acierto'
                    ],

                riesgo=
                    riesgo,

                tendencia=
                    tendencia
            )
        )


        # DASHBOARD

        dashboard = (

            DashboardDataService
            .preparar_dashboard(

                metricas=
                    metricas,

                errores=
                    errores,

                perfil=
                    perfil
            )
        )


        # CONSOLIDACIÓN FINAL

        resultado_final = (

            ResultConsolidationService
            .consolidar(

                analisis=
                    resumen_estudiante,

                metricas=
                    metricas,

                errores=
                    errores,

                perfil=
                    perfil,

                alertas=
                    alertas,

                resumen=
                    resumen
            )
        )


        # DATOS EXTRA

        resultado_final[
            'riesgo'
        ] = riesgo


        resultado_final[
            'tendencia'
        ] = tendencia


        resultado_final[
            'plan_refuerzo'
        ] = plan_refuerzo


        resultado_final[
            'dashboard'
        ] = dashboard


        return resultado_final