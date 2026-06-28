from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


class PDFReportService:


    @staticmethod
    def generar_reporte(


        resultado,

        ruta_pdf
    ):


        doc = SimpleDocTemplate(

            ruta_pdf,

            pagesize=letter
        )


        elementos = []


        estilos = getSampleStyleSheet()


        # =================================================
        # TÍTULO
        # =================================================

        titulo = Paragraph(

            'I.E Elvira García y García',

            estilos['Title']
        )


        elementos.append(
            titulo
        )


        elementos.append(
            Spacer(1, 20)
        )


        # =================================================
        # DESCRIPCIÓN
        # =================================================

        descripcion = Paragraph(

            'Reporte generado automáticamente '
            'por el sistema inteligente '
            'de análisis matemático I.E Elvira García Y García.',

            estilos['BodyText']
        )


        elementos.append(
            descripcion
        )


        elementos.append(
            Spacer(1, 20)
        )


        # =================================================
        # TABLA
        # =================================================

        datos = [

            ['Campo', 'Valor'],

            [
                'Resultado',

                'Correcto'
                if resultado.es_correcto
                else 'Incorrecto'
            ],

            [
                'Confianza OCR',

                f'{resultado.nivel_confianza}%'
            ],

            [
                'Tipo Error',

                resultado.tipo_error
            ],

            [
                'Dificultad',

                resultado.dificultad
            ],

            [
                'Riesgo Académico',

                resultado.riesgo_academico
            ],

            [
                'Tema Matemático',

                resultado.tema_matematico
            ],

            [
                'Recomendación',

                resultado.recomendacion
            ]
        ]


        tabla = Table(

            datos,

            colWidths=[180, 320]
        )


        tabla.setStyle(

            TableStyle([

                (
                    'BACKGROUND',

                    (0, 0),

                    (-1, 0),

                    colors.HexColor('#2563eb')
                ),

                (
                    'TEXTCOLOR',

                    (0, 0),

                    (-1, 0),

                    colors.white
                ),

                (
                    'GRID',

                    (0, 0),

                    (-1, -1),

                    1,

                    colors.grey
                ),

                (
                    'FONTNAME',

                    (0, 0),

                    (-1, 0),

                    'Helvetica-Bold'
                ),

                (
                    'BOTTOMPADDING',

                    (0, 0),

                    (-1, 0),

                    12
                ),

                (
                    'BACKGROUND',

                    (0, 1),

                    (-1, -1),

                    colors.whitesmoke
                )
            ])
        )


        elementos.append(
            tabla
        )


        elementos.append(
            Spacer(1, 30)
        )


        # =================================================
        # PIE
        # =================================================

        pie = Paragraph(

            'I.E Elvira García y García - '
            'Reporte generado automáticamente.',

            estilos['Italic']
        )


        elementos.append(
            pie
        )


        # =================================================
        # BUILD
        # =================================================

        doc.build(
            elementos
        )