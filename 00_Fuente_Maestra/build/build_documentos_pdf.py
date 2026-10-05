"""
Oryzz · renderiza las versiones PDF (ejemplo) de 07_Documentos desde _fuente/html.

    python build_documentos_pdf.py            # todos
    python build_documentos_pdf.py 01 05      # solo los que empiezan por 01 y 05
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render import html_to_pdf

DOCS = os.path.normpath(os.path.join(HERE, '..', '..', '07_Documentos'))
SRC = os.path.join(DOCS, '_fuente', 'html')

MAPA = {
    '01_propuesta-comercial.html':   ('01_Propuesta_Comercial', 'Oryzz_Propuesta-Comercial_EJEMPLO.pdf'),
    '02_informe-diagnostico.html':   ('02_Informe_Diagnostico', 'Oryzz_Informe-Diagnostico_EJEMPLO.pdf'),
    '03_informe-mensual.html':       ('03_Informe_Mensual', 'Oryzz_Informe-Mensual_EJEMPLO.pdf'),
    '04_caso-de-estudio.html':       ('04_Caso_de_Estudio', 'Oryzz_Caso-de-Estudio_EJEMPLO.pdf'),
    '05_presupuesto.html':           ('05_Presupuesto_y_Factura', 'Oryzz_Presupuesto_EJEMPLO.pdf'),
    '05_factura.html':               ('05_Presupuesto_y_Factura', 'Oryzz_Factura_EJEMPLO.pdf'),
    '06_carta.html':                 ('06_Carta_y_Membrete', 'Oryzz_Carta_EJEMPLO.pdf'),
    '06_documento-en-blanco.html':   ('06_Carta_y_Membrete', 'Oryzz_Documento-en-blanco.pdf'),
    '07_brief-onboarding.html':      ('07_Brief_Onboarding', 'Oryzz_Brief-Onboarding.pdf'),
    '08_one-pager-servicios.html':   ('08_One_Pagers', 'Oryzz_One-Pager-Servicios.pdf'),
    '08_one-pager-tap.html':         ('08_One_Pagers', 'Oryzz-Tap_One-Pager.pdf'),
    '09_contrato-servicios.html':    ('09_Contrato_de_Servicios', 'Oryzz_Contrato-Servicios_MAQUETA.pdf'),
}

if __name__ == '__main__':
    filtro = sys.argv[1:]
    for src, (carpeta, nombre) in MAPA.items():
        if filtro and not any(src.startswith(f) for f in filtro):
            continue
        out = os.path.join(DOCS, carpeta, nombre)
        html_to_pdf(os.path.join(SRC, src), out)
        print('ok', out)
