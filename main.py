from sensor.reader import YieryiSensor
from agronomy.recommendation_engine import RecommendationEngine
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_pdf(report_text):
    filename = "reporte_agraria.pdf"
    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    for line in report_text.split("\n"):
        elements.append(Paragraph(line, style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return filename


def main():

    sensor = YieryiSensor("COM3")
    sample = sensor.read_sample()

    hectares = float(input("Ingrese tamaño del cultivo (ha): "))
    already_planted = input("¿Ya sembró? (s/n): ")

    if already_planted.lower() == "s":
        sowing_date = datetime.strptime(
            input("Fecha siembra (YYYY-MM-DD): "), "%Y-%m-%d"
        )
    else:
        sowing_date = None

    report = RecommendationEngine.generate(sample, hectares, sowing_date)

    print("\n==============================")
    print("        REPORTE AGRARIA")
    print("==============================\n")
    print(report)

    generate = input("\n¿Generar PDF? (s/n): ")

    if generate.lower() == "s":
        pdf_file = generate_pdf(report)
        print(f"\nPDF generado: {pdf_file}")


if __name__ == "__main__":
    main()