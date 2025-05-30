
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import requests
from io import BytesIO

def generate_portada_pdf(cliente_nombre: str, output_path: str):
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    azul_endress = colors.HexColor('#0B5CBD')
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)

    c.drawCentredString(width / 2, height - 100, "Products Solutions Service")
    c.line(70, height - 105, width - 70, height - 105)

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 140, "LIBRO DE PROYECTO")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 170, cliente_nombre)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(70, height - 210, "PROYECTO:")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 230,
        "Sistema de Transmisión y Recolección de Datos para el Consumo de Agua en Pozos")
    c.drawCentredString(width / 2, height - 245,
        "para Cumplimiento de Norma Mexicana NMX-AA-179-SCFI-2018")

    try:
        img_url = "https://www.es.endress.com/__image/a/8742097/k/79b49db74c3a008851b6280623bd308670ba747d/ar/16-9/w/771/t/jpg/b/ffffff/fn/Water-Energy-Monitoring-I7A8561.jpg"
        response = requests.get(img_url)
        medidor_img = ImageReader(BytesIO(response.content))
        c.drawImage(medidor_img, 70, height - 420, width=width - 140, height=120,
                    preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Error al cargar imagen del medidor: {e}")

    c.setFillColor(azul_endress)
    c.rect(0, 0, width, 40, fill=True, stroke=False)

    try:
        logo_url = "https://w7.pngwing.com/pngs/1011/907/png-transparent-endress-hauser-hd-logo.png"
        response = requests.get(logo_url)
        logo_img = ImageReader(BytesIO(response.content))
        c.drawImage(logo_img, width - 160, 10, width=120, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Error al cargar logo: {e}")

    c.save()
