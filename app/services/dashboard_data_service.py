class DashboardDataService:


    @staticmethod
    def preparar_dashboard(


        metricas,

        errores,

        perfil
    ):


        return {

            'cards': {

                'porcentaje_correctos':

                    metricas.get(
                        'porcentaje_correctos',
                        0
                    ),

                'total_errores':

                    sum(
                        errores.values()
                    )

                    if errores else 0,

                'nivel_general':

                    perfil.get(
                        'nivel_general',
                        'intermedio'
                    )
            },


            'graficos': {

                'errores':

                    errores
            }
        }