# app.py
from io import BytesIO
from flask import Flask, render_template, request, abort, send_file, jsonify
from flask_cors import CORS
import time

# Helpers / Pages
from utils.helpers import getDriver
from pages.loginPage import LoginPage
from pages.menuPageConsultaComprobante import MenuPage as MenuCompPage
from pages.formPageConsultaComprobante import FormPage as FormCompPage
from pages.downloadConsultaComprobante import DownloadPage as DownloadCompPage

from pages.menuPageConsultaGuia import MenuPage as MenuGuiaPage
from pages.formPageConsultaGuia import FormPage as FormGuiaPage
from pages.downloadConsultaGuia import DownloadPage as DownloadGuiaPage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --------- Orquestadores ----------
def runConsultaComprobante(rucEmisor: str, serie: str, correlativo: str):
    """Retorna (filename, BytesIO, mimetype) o (None, None, None)."""
    driver = getDriver()
    try:
        LoginPage().login(driver)
        MenuCompPage().goToConsultaComprobantes(driver)
        FormCompPage().goToForm(driver, rucEmisor, serie, correlativo)
        return DownloadCompPage().downloadXML(driver)
    finally:
        try:
            driver.quit()
        except Exception:
            pass

def runConsultaGuia(rucEmisor: str, serie: str, numero: str):
    """Retorna (filename, BytesIO, mimetype) o (None, None, None)."""
    driver = getDriver()
    try:
        LoginPage().login(driver)
        MenuGuiaPage().goToGuiasRemision(driver)
        time.sleep(5)
        FormGuiaPage().goToForm(driver, serie, numero)  # tu FormPage usa (serie, numero)
        return DownloadGuiaPage().downloadXML(driver)
    finally:
        try:
            driver.quit()
        except Exception:
            pass

# --------- Rutas ----------
@app.get('/')
def index():
    return render_template('index.html')

@app.post('/api/comprobantes')
def apiComprobantes():
    data = request.get_json(force=True, silent=True) or {}
    ruc = data.get('rucEmisor') or data.get('ruc')
    serie = data.get('serie')
    correlativo = data.get('correlativo')
    if not all([ruc, serie, correlativo]):
        abort(400, description="Parámetros requeridos: rucEmisor (o ruc), serie, correlativo.")

    filename, bio, mime = runConsultaComprobante(ruc, serie, correlativo)
    if not filename or not bio:
        abort(500, description="No se pudo descargar el XML del comprobante.")
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name=filename, mimetype=mime)

@app.post('/api/guias')
def apiGuias():
    data = request.get_json(force=True, silent=True) or {}
    # Para guías NO pedimos RUC
    serie = data.get('serie')
    numero = data.get('numero') or data.get('correlativo')

    if not all([serie, numero]):
        abort(400, description="Parámetros requeridos: serie y numero/correlativo.")

    filename, bio, mime = runConsultaGuia("", serie, numero)  # Pasamos RUC vacío
    if not filename or not bio:
        abort(500, description="No se pudo descargar el XML de la guía.")
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name=filename, mimetype=mime)


@app.get('/health')
def health():
    return jsonify(ok=True), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
