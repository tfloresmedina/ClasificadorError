class PedagogicalAlertService:


    @staticmethod
    def generar_alertas(


        riesgo,

        tendencia
    ):


        alertas = []


        # ALERTA DE RIESGO

        if riesgo == 'alto':

            alertas.append(

                'Estudiante con alto riesgo académico.'
            )


        # ALERTA DE TENDENCIA

        if tendencia == 'descenso':

            alertas.append(

                'Se detecta descenso en el rendimiento.'
            )


        # ALERTA COMBINADA

        if (

            riesgo == 'alto'

            and

            tendencia == 'descenso'
        ):

            alertas.append(

                'Requiere intervención pedagógica inmediata.'
            )


        return alertas