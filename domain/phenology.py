from datetime import datetime

class Phenology:

    @staticmethod
    def get_stage(sowing_date):
        today = datetime.today()
        das = (today - sowing_date).days

        if das <= 10:
            return "Germinacion"
        elif das <= 30:
            return "V3-V4"
        elif das <= 60:
            return "V5-V10"
        elif das <= 85:
            return "V11-VT"
        elif das <= 100:
            return "Floracion"
        elif das <= 135:
            return "Llenado"
        else:
            return "Madurez"