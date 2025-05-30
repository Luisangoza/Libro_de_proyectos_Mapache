
import streamlit as st
from PyPDF2 import PdfMerger
import tempfile
import os
from pdf_generator import generate_portada_pdf

st.set_page_config(page_title="Generador de Portadas - Endress+Hauser", layout="centered")

st.title("📘 Generador de Libro de Proyecto")
st.subheader("Endress+Hauser | Products Solutions Services")

cliente = st.text_input("Nombre del cliente", max_chars=100)
uploaded_files = st.file_uploader("Cargar archivos PDF", type=["pdf"], accept_multiple_files=True)

if st.button("Generar Libro de Proyecto") and cliente and uploaded_files:
    with st.spinner("Generando portada y uniendo PDFs..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            portada_path = os.path.join(tmpdir, "portada.pdf")
            generate_portada_pdf(cliente, portada_path)

            merger = PdfMerger()
            merger.append(portada_path)

            for pdf in uploaded_files:
                file_path = os.path.join(tmpdir, pdf.name)
                with open(file_path, "wb") as f:
                    f.write(pdf.read())
                merger.append(file_path)

            final_path = os.path.join(tmpdir, f"Libro_Proyecto_{cliente}.pdf")
            merger.write(final_path)
            merger.close()

            with open(final_path, "rb") as f:
                st.success("✅ Libro generado correctamente")
                st.download_button("📥 Descargar Libro PDF", f, file_name=f"Libro_Proyecto_{cliente}.pdf")
else:
    st.info("Por favor ingresa el nombre del cliente y carga al menos un PDF.")
