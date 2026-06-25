from datetime import datetime


class LoggingService:


    @staticmethod
    def generar_log(


        tipo_evento,

        detalle
    ):


        return {

            'timestamp':

                datetime.now()
                .strftime(

                    '%Y-%m-%d %H:%M:%S'
                ),

            'tipo_evento':
                tipo_evento,

            'detalle':
                detalle
        }