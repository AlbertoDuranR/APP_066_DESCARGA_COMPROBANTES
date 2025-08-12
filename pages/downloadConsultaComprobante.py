# pages/downloadConsultaComprobante.py
import os
import time
import mimetypes
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.waits import waitVisible

class DownloadPage:
    def _switchToIframe(self, driver, timeout=25):
        # entra al iframe donde está el modal
        try:
            driver.switch_to.frame("iframeApplication")
        except Exception:
            iframe = waitVisible(driver, (By.ID, "iframeApplication"))
            driver.switch_to.frame(iframe)

    def _enableDownloads(self, driver, downloadDir):
        os.makedirs(downloadDir, exist_ok=True)
        try:
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": downloadDir
            })
        except Exception:
            # si no soporta CDP, seguirá con su config por defecto
            pass

    def _waitNewFileStable(self, downloadDir, previousSet, timeout=30):
        """Espera un archivo NUEVO (no .crdownload) y que su tamaño se estabilice."""
        end = time.time() + timeout
        while time.time() < end:
            current = {f for f in os.listdir(downloadDir) if not f.endswith(".crdownload")}
            newFiles = list(current - previousSet)
            if newFiles:
                newFiles.sort(key=lambda f: os.path.getmtime(os.path.join(downloadDir, f)), reverse=True)
                candidate = os.path.join(downloadDir, newFiles[0])

                lastSize = -1
                stableEnd = time.time() + 6
                while time.time() < stableEnd:
                    try:
                        size = os.path.getsize(candidate)
                    except FileNotFoundError:
                        break
                    if size == lastSize and size > 0:
                        return os.path.abspath(candidate)
                    lastSize = size
                    time.sleep(0.35)
            time.sleep(0.35)
        return None

    def downloadXML(self, driver, timeout=25):
        """
        Hace click en «Descargar XML», espera el archivo, lo lee en memoria y retorna:
        (filename, BytesIO, mimetype). Si falla, retorna (None, None, None).
        """
        downloadDir = os.path.abspath("temp")
        self._enableDownloads(driver, downloadDir)
        self._switchToIframe(driver, timeout=timeout)

        # modal visible y sin spinner
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ngb-modal-window .modal-content"))
        )
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "ngx-spinner"))
        )

        before = {f for f in os.listdir(downloadDir) if not f.endswith(".crdownload")}

        # botón «Descargar XML»
        btnXml = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//ngb-modal-window//button[@ngbtooltip='Descargar XML']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnXml)
        driver.execute_script("arguments[0].click();", btnXml)

        filePath = self._waitNewFileStable(downloadDir, before, timeout=40)
        if not filePath:
            return None, None, None

        filename = os.path.basename(filePath)
        mime, _ = mimetypes.guess_type(filename)
        mime = mime or "application/xml"

        with open(filePath, "rb") as f:
            data = f.read()

        # Limpia disco (solo pasaje temporal)
        try:
            os.remove(filePath)
        except Exception:
            pass

        return filename, BytesIO(data), mime
