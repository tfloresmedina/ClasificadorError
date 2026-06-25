class ReinforcementPlanningService:


    @staticmethod
    def generar_plan(


        debilidad,

        riesgo
    ):


        plan = []


        # REFUERZO SEGÚN DEBILIDAD

        if debilidad == 'error_signos':

            plan.append(

                'Practicar operaciones con signos.'
            )


        if debilidad == 'error_distributiva':

            plan.append(

                'Resolver ejercicios de distributiva.'
            )


        if debilidad == 'fracciones':

            plan.append(

                'Reforzar simplificación de fracciones.'
            )


        if debilidad == 'variables_invalidas':

            plan.append(

                'Revisar uso correcto de variables.'
            )


        # REFUERZO SEGÚN RIESGO

        if riesgo == 'alto':

            plan.append(

                'Asignar acompañamiento personalizado.'
            )


        if riesgo == 'medio':

            plan.append(

                'Incrementar práctica semanal.'
            )


        return plan