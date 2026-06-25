class StepDetectorService:


    @staticmethod
    def contar_pasos(
        ejercicio
    ):

        if not ejercicio:

            return 0

        return len(
            ejercicio
        )