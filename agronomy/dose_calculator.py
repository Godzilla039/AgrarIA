class DoseCalculator:

    @staticmethod
    def ppm_to_kg(ppm):
        return ppm * 2.5

    @staticmethod
    def calculate_deficit(current, target):
        deficit_ppm = target - current
        return deficit_ppm * 2.5 if deficit_ppm > 0 else 0

    @staticmethod
    def kg_n_to_urea(kg_n):
        return kg_n / 0.46

    @staticmethod
    def kg_p_to_map(kg_p2o5):
        return kg_p2o5 / 0.52

    @staticmethod
    def kg_k_to_kcl(kg_k2o):
        return kg_k2o / 0.60