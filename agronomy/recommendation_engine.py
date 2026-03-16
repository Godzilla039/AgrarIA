from domain.classification import SoilClassifier
from agronomy.dose_calculator import DoseCalculator
from domain.phenology import Phenology
from datetime import datetime, timedelta

class RecommendationEngine:

    @staticmethod
    def generate(sample, hectares, sowing_date=None):

        lines = []
        today = datetime.today()

        ph = sample["ph"]
        n = sample["n"]
        p = sample["p"]
        k = sample["k"]
        ce = sample["ec"]
        humidity = sample["humidity"]
        temperature = sample["temperature"]

        # =============================
        # ETAPA
        # =============================
        if sowing_date:
            stage = Phenology.get_stage(sowing_date)
            lines.append(f"🌱 Etapa actual del cultivo: {stage}")
        else:
            stage = "Pre-siembra"
            lines.append("🌱 Cultivo aún no sembrado.")

        # =============================
        # DIAGNÓSTICO
        # =============================
        ph_class = SoilClassifier.classify_ph(ph)
        n_class = SoilClassifier.classify_n(n)
        p_class = SoilClassifier.classify_p(p)
        k_class = SoilClassifier.classify_k(k)

        lines.append("\n📊 DIAGNÓSTICO DEL SUELO:")
        lines.append(f"- pH: {ph} → {ph_class}")
        lines.append(f"- Nitrógeno: {n} ppm → {n_class}")
        lines.append(f"- Fósforo: {p} ppm → {p_class}")
        lines.append(f"- Potasio: {k} ppm → {k_class}")
        lines.append(f"- CE: {ce} dS/m")
        lines.append(f"- Humedad: {humidity}%")
        lines.append(f"- Temperatura suelo: {temperature} °C")

        # =============================
        # TEMPERATURA PARA SIEMBRA
        # =============================
        if not sowing_date and temperature < 10:
            lines.append(
                "\n⚠ Temperatura del suelo menor a 10°C. "
                "No se recomienda sembrar aún."
            )

        # =============================
        # ENCALADO
        # =============================
        if ph_class == "CRITICO" and not sowing_date:

            cal_ton = 3
            total_cal = round(cal_ton * hectares, 2)

            lines.append(
                "\n🔹 CORRECCIÓN DE pH:"
                f"\nAplicar {cal_ton} t/ha de cal agrícola "
                f"(Total lote: {total_cal} t)."
                "\n- Aplicar a voleo."
                "\n- Incorporar a 15–20 cm."
                "\n- No aplicar urea en los siguientes 15–20 días."
            )

        # =============================
        # CE
        # =============================
        ce_risk = False

        if ce > 4.0:
            ce_risk = True
            lines.append(
                "\n🚨 CE > 4.0 dS/m (ALTO RIESGO)."
                "\n- Realizar riego lixiviante."
                "\n- Mejorar drenaje."
                "\n- Incorporar materia orgánica."
                "\n- Evitar KCl."
            )
        elif ce > 2.5:
            ce_risk = True
            lines.append(
                "\n⚠ CE entre 2.5–4.0 dS/m."
                "\n- Fraccionar fertilización."
                "\n- Evitar grandes dosis puntuales de KCl y urea."
            )

        # =============================
        # NITRÓGENO
        # =============================
        if n_class == "CRITICO":
            kg_n = 140
        elif n_class == "BAJO":
            kg_n = 100
        elif n_class == "OPTIMO":
            kg_n = 60
        else:
            kg_n = 30

        urea_ha = round(DoseCalculator.kg_n_to_urea(kg_n), 1)
        total_urea = round(urea_ha * hectares, 2)

        lines.append(
            f"\n🔹 NITRÓGENO (Urea 46%):"
            f"\n- {urea_ha} kg/ha (Total lote: {total_urea} kg)."
            "\n- Aplicar en V3–V4 y V6–V8."
            "\n- Aplicar entre surcos."
            "\n- Antes de lluvia o riego."
        )

        # =============================
        # FÓSFORO
        # =============================
        if not sowing_date:
            if p_class == "CRITICO":
                kg_p = 70
            elif p_class == "BAJO":
                kg_p = 60
            elif p_class == "OPTIMO":
                kg_p = 40
            else:
                kg_p = 25

            map_ha = round(DoseCalculator.kg_p_to_map(kg_p), 1)
            total_map = round(map_ha * hectares, 2)

            lines.append(
                f"\n🔹 FÓSFORO (MAP 11-52-0):"
                f"\n- {map_ha} kg/ha (Total lote: {total_map} kg)."
                "\n- Aplicar 100% a la siembra."
                "\n- Banda localizada 3–5 cm al lado y 3–5 cm debajo de la semilla."
            )
        else:
            lines.append(
                "\n🔹 FÓSFORO:"
                "\nNo se recomienda aplicar fósforo después de la emergencia."
            )

        # =============================
        # POTASIO
        # =============================
        if k_class in ["CRITICO", "BAJO"]:
            kg_k = 120
        else:
            kg_k = 60

        if ce_risk:
            k2so4_ha = round(kg_k / 0.50, 1)
            total_k2so4 = round(k2so4_ha * hectares, 2)

            lines.append(
                f"\n🔹 POTASIO (Sulfato de Potasio 0-0-50):"
                f"\n- {k2so4_ha} kg/ha (Total lote: {total_k2so4} kg)."
                "\n- Aplicar 50% a la siembra y 50% en V4–V6."
            )
        else:
            kcl_ha = round(DoseCalculator.kg_k_to_kcl(kg_k), 1)
            total_kcl = round(kcl_ha * hectares, 2)

            lines.append(
                f"\n🔹 POTASIO (KCl 0-0-60):"
                f"\n- {kcl_ha} kg/ha (Total lote: {total_kcl} kg)."
                "\n- Aplicar 50% a la siembra y 50% en V4–V6."
            )

        # =============================
        # HUMEDAD
        # =============================
        if humidity < 15:
            lines.append("\n💧 Suelo seco. Recomendado riego ligero.")
        elif humidity > 40:
            lines.append("\n💧 Suelo muy húmedo. Evitar riego.")
        else:
            lines.append("\n💧 Humedad adecuada.")

        # =============================
        # CÁLCULO MULTIVARIABLE DE FECHA
        # =============================
        if not sowing_date:

            min_delay = 0
            ideal_delay = 0
            max_delay = 0
            reasons = []

            if ph < 5.5:
                min_delay = max(min_delay, 30)
                ideal_delay = max(ideal_delay, 45)
                max_delay = max(max_delay, 60)
                reasons.append("Corrección de pH")

            if temperature < 10:
                min_delay = max(min_delay, 7)
                ideal_delay = max(ideal_delay, 14)
                max_delay = max(max_delay, 21)
                reasons.append("Temperatura baja")

            if ce > 4.0:
                min_delay = max(min_delay, 20)
                ideal_delay = max(ideal_delay, 30)
                max_delay = max(max_delay, 40)
                reasons.append("CE muy alta")
            elif ce > 2.5:
                min_delay = max(min_delay, 10)
                ideal_delay = max(ideal_delay, 15)
                max_delay = max(max_delay, 20)
                reasons.append("CE moderadamente alta")

            if humidity < 15:
                min_delay = max(min_delay, 2)
                ideal_delay = max(ideal_delay, 3)
                max_delay = max(max_delay, 5)
                reasons.append("Suelo seco")

            if min_delay == 0:
                lines.append("\n✅ Condiciones adecuadas para sembrar ahora.")
            else:
                min_date = today + timedelta(days=min_delay)
                ideal_date = today + timedelta(days=ideal_delay)
                max_date = today + timedelta(days=max_delay)

                lines.append(
                    "\n📅 FECHA ESTIMADA DE SIEMBRA:"
                    f"\n- Fecha mínima técnica: {min_date.date()}"
                    f"\n- Fecha ideal recomendada: {ideal_date.date()}"
                    f"\n- Fecha máxima técnica: {max_date.date()}"
                    "\nFactores considerados:"
                )

                for r in reasons:
                    lines.append(f"- {r}")

        return "\n".join(lines)