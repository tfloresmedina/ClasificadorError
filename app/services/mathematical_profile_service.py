class MathematicalProfileService:


    @staticmethod
    def construir_perfil(


        porcentaje_acierto,

        errores_frecuentes,

        dificultad_promedio
    ):


        perfil = {


            'nivel_general':
            'intermedio',


            'fortaleza':
            'aritmetica',


            'debilidad':
            'algebra'
        }


        # NIVEL GENERAL

        if porcentaje_acierto >= 80:

            perfil[
                'nivel_general'
            ] = 'avanzado'


        elif porcentaje_acierto < 50:

            perfil[
                'nivel_general'
            ] = 'basico'


        # DEBILIDAD PRINCIPAL

        if errores_frecuentes:

            perfil[
                'debilidad'
            ] = max(

                errores_frecuentes,

                key=
                errores_frecuentes.get
            )


        # FORTALEZA

        if dificultad_promedio == 'alta':

            perfil[
                'fortaleza'
            ] = 'resolucion_compleja'


        return perfil