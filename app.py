
import streamlit as st
from PyPDF2 import PdfMerger
from fpdf import FPDF
import os

COLOR_AZUL = (11, 92, 189)

class PDF(FPDF):
    def header(self):
        pass
    def footer(self):
        pass

    def portada_principal(self, cliente, codigo_libro, imagen_medidor_path, logo_path):
        self.add_page()
        self.set_fill_color(*COLOR_AZUL)
        self.rect(10, 10, 5, 277, 'F')

        self.set_font("Arial", '', 11)
        self.set_xy(20, 20)
        self.cell(0, 10, "        Products     Solutions     Service", ln=True, align='C')

        self.set_draw_color(0, 0, 0)
        self.line(20, 30, 200, 30)

        self.set_font("Arial", 'B', 20)
        self.set_xy(20, 40)
        self.cell(0, 10, "LIBRO DE PROYECTO", ln=True, align='C')

        self.set_font("Arial", '', 14)
        self.cell(0, 10, cliente, ln=True, align='C')

        self.set_xy(20, 70)
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, "PROYECTO:", ln=True, align='L')

        self.set_font("Arial", '', 11)
        self.multi_cell(0, 8,
                        "Sistema de Transmisión y Recolección de Datos para el Consumo de Agua en Pozos "
                        "para Cumplimiento de Norma Mexicana NMX-AA-179-SCFI-2018", align='C')

        if imagen_medidor_path:
            self.image(imagen_medidor_path, x=45, y=120, w=160, h=90)
        if logo_path:
            self.image(logo_path, x=80, y=250, w=50)

        self.set_font("Arial", '', 11)
        self.set_xy(20, 240)
        self.cell(0, 10, f"Código del libro: {codigo_libro}", ln=True, align='C')

    def generar_indice(self, archivos):
        self.add_page()
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "ÍNDICE DE DOCUMENTOS", ln=True, align='C')
        self.ln(10)
        self.set_font("Arial", '', 12)
        for i, archivo in enumerate(archivos, 1):
            self.cell(0, 10, f"{i}. {archivo.name}", ln=True, align='L')

st.title("📘 Generador de Libro de Proyectos Mapache")
cliente = st.text_input("Nombre del cliente")
codigo = st.text_input("Código del libro a generar")
imagen_medidor = st.file_uploader("Imagen del medidor", type=["png", "jpg"])
logo = st.file_uploader("Logo de Endress+Hauser", type=["png", "jpg"])
archivos = st.file_uploader("Sube tus archivos PDF", type=["pdf"], accept_multiple_files=True)

if st.button("Generar Libro PDF") and archivos and cliente and codigo:
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    medidor_path = "temp_medidor.jpg"
    logo_path = "temp_logo.png"
    if imagen_medidor: open(medidor_path, "wb").write(imagen_medidor.read())
    if logo: open(logo_path, "wb").write(logo.read())

    pdf.portada_principal(cliente, codigo, medidor_path if imagen_medidor else "", logo_path if logo else "")
    pdf.generar_indice(archivos)

    output_path = "Libro_de_proyectos_Mapache_generado.pdf"
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 Descargar PDF generado", f, file_name=output_path)
    if imagen_medidor: os.remove(medidor_path)
    if logo: os.remove(logo_path)
