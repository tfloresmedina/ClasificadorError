class ConfidenceScoreService:


    @staticmethod
    def calcular_score(
        confianza_ocr,
        ruido_detectado=False,
        autocorregido=False,
        correcto=False
    ):


        score = (
            confianza_ocr
        )


        # penalización por ruido OCR

        if ruido_detectado:

            score -= 15


        # penalización por autocorrección

        if autocorregido:

            score -= 10


        # bonus si SymPy validó correcto

        if correcto:

            score += 5


        # límites

        if score > 100:

            score = 100


        if score < 0:

            score = 0


        return round(score, 2)