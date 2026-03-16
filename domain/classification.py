class SoilClassifier:

    @staticmethod
    def classify_ph(ph):
        if ph < 5.5:
            return "CRITICO"
        elif 5.5 <= ph < 6.0:
            return "BAJO"
        elif 6.0 <= ph <= 7.0:
            return "OPTIMO"
        elif 7.0 < ph <= 7.2:
            return "BUENO"
        else:
            return "NO_RECOMENDADO"

    @staticmethod
    def classify_n(n):
        if n < 10:
            return "CRITICO"
        elif 10 <= n < 18:
            return "BAJO"
        elif 18 <= n <= 25:
            return "OPTIMO"
        elif 25 < n <= 30:
            return "BUENO"
        else:
            return "ALTO"

    @staticmethod
    def classify_p(p):
        if p < 15:
            return "CRITICO"
        elif 15 <= p < 25:
            return "BAJO"
        elif 25 <= p <= 35:
            return "OPTIMO"
        elif 35 < p <= 50:
            return "BUENO"
        else:
            return "ALTO"

    @staticmethod
    def classify_k(k):
        if k < 100:
            return "CRITICO"
        elif 100 <= k < 165:
            return "BAJO"
        elif 165 <= k <= 250:
            return "OPTIMO"
        elif 250 < k <= 600:
            return "BUENO"
        else:
            return "ALTO"