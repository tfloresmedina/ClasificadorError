class PipelineTraceService:


    @staticmethod
    def generar_trace(


        resultado_ocr,

        resultado_final
    ):


        pasos = []


        # =============================================
        # OCR
        # =============================================

        pasos.append({

            'titulo':
                'OCR Inteligente',

            'descripcion':

                'Extracción automática '
                'de texto matemático '
                'desde imagen.',

            'estado':
                'completado'
        })


        # =============================================
        # NORMALIZACIÓN
        # =============================================

        pasos.append({

            'titulo':
                'Normalización Algebraica',

            'descripcion':

                'Limpieza y transformación '
                'de expresiones matemáticas.',

            'estado':
                'completado'
        })


        # =============================================
        # AST
        # =============================================

        pasos.append({

            'titulo':
                'Análisis AST',

            'descripcion':

                'Construcción del árbol '
                'sintáctico algebraico.',

            'estado':
                'completado'
        })


        # =============================================
        # SYMPY
        # =============================================

        pasos.append({

            'titulo':
                'Validación SymPy',

            'descripcion':

                'Comparación simbólica '
                'y equivalencia algebraica.',

            'estado':
                'completado'
        })


        # =============================================
        # ERROR
        # =============================================

        pasos.append({

            'titulo':
                'Clasificación Error',

            'descripcion':

                'Detección automática '
                'de inconsistencias '
                'matemáticas.',

            'estado':
                'completado'
        })


        # =============================================
        # PEDAGOGÍA
        # =============================================

        pasos.append({

            'titulo':
                'Recomendación Pedagógica',

            'descripcion':

                'Generación de alertas '
                'y recomendaciones '
                'académicas.',

            'estado':
                'completado'
        })


        return pasos