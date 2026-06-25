from datetime import datetime

from app.database.connection import db


class ResultadoAnalisis(db.Model):


    __tablename__ = 'resultados_analisis'


    # =====================================================
    # ID
    # =====================================================

    id = db.Column(

        db.Integer,

        primary_key=True
    )


    # =====================================================
    # EXPRESIONES
    # =====================================================

    expresion_original = db.Column(

        db.Text,

        nullable=True
    )


    expresion_procesada = db.Column(

        db.Text,

        nullable=True
    )


    expresion_sympy = db.Column(

        db.Text,

        nullable=True
    )


    # =====================================================
    # RESULTADO PRINCIPAL
    # =====================================================

    es_correcto = db.Column(

        db.Boolean,

        default=False
    )


    porcentaje_coincidencia = db.Column(

        db.Float,

        default=0
    )


    nivel_confianza = db.Column(

        db.Float,

        default=0
    )


    estado_analisis = db.Column(

        db.String(30),

        default='pendiente'
    )


    # =====================================================
    # ERROR Y PEDAGOGÍA
    # =====================================================

    tipo_error = db.Column(

        db.String(100),

        nullable=True
    )


    severidad_error = db.Column(

        db.String(30),

        nullable=True
    )


    descripcion_error = db.Column(

        db.Text,

        nullable=True
    )


    recomendacion = db.Column(

        db.Text,

        nullable=True
    )


    observaciones = db.Column(

        db.Text,

        nullable=True
    )


    # =====================================================
    # ANÁLISIS MATEMÁTICO
    # =====================================================

    tema_matematico = db.Column(

        db.String(100),

        nullable=True
    )


    tipo_ejercicio = db.Column(

        db.String(100),

        nullable=True
    )


    dificultad = db.Column(

        db.String(50),

        nullable=True
    )


    pasos_estimados = db.Column(

        db.Integer,

        default=0
    )


    # =====================================================
    # MÉTRICAS PEDAGÓGICAS
    # =====================================================

    riesgo_academico = db.Column(

        db.String(30),

        nullable=True
    )


    tendencia_aprendizaje = db.Column(

        db.String(30),

        nullable=True
    )


    perfil_matematico = db.Column(

        db.String(100),

        nullable=True
    )

    competencia = db.Column(

        db.String(150),

        nullable=True
    )


    fase_polya = db.Column(

        db.String(100),

        nullable=True
    )
    
    detalle_procedimiento = db.Column(

        db.Text,

        nullable=True
    )
    # =====================================================
    # OCR
    # =====================================================

    ruido_ocr = db.Column(

        db.Boolean,

        default=False
    )


    autocorreccion_aplicada = db.Column(

        db.Boolean,

        default=False
    )


    # =====================================================
    # RELACIÓN
    # =====================================================

    respuesta_alumno_id = db.Column(

        db.Integer,

        db.ForeignKey(
            'respuestas_alumno.id'
        ),

        nullable=False,

        unique=True
    )


    # =====================================================
    # FECHAS
    # =====================================================

    fecha_registro = db.Column(

        db.DateTime,

        default=datetime.utcnow
    )


    # =====================================================
    # REPRESENTACIÓN
    # =====================================================

    def __repr__(self):

        return (

            f'<ResultadoAnalisis {self.id}>'
        )

    # =====================================================
    # INTERPRETACIÓN CURRICULAR
    # =====================================================

    capacidad_curricular = db.Column(

        db.String(250),

        nullable=True
    )

    desempeno_curricular = db.Column(

        db.Text,

        nullable=True
    )

    nivel_logro = db.Column(

        db.String(50),

        nullable=True
    )

    recomendacion_curricular = db.Column(

        db.Text,

        nullable=True
    )

    # =====================================================
    # COMPARACIÓN MODELO
    # =====================================================

    coincidencia_modelo = db.Column(

        db.Float,

        default=0
    )

    paso_error_modelo = db.Column(

        db.Integer,

        nullable=True
    )

    procedimiento_detectado = db.Column(

    db.Text,

    nullable=True
    )