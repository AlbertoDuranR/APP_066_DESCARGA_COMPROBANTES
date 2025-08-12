# pages/downloadConsultaGuia.py
import os
import time
import mimetypes
from io import BytesIO
from utils.waits import waitVisible, waitClickable
from selenium.webdriver.common.by import By

class DownloadPage:
    def _enableDownloads(self, driver, downloadDir):
        os.makedirs(downloadDir, exist_ok=True)
        try:
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": downloadDir
            })
        except Exception:
            pass

    def _waitNewFileStable(self, downloadDir, previousSet, timeout=30):
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

    def downloadXML(self, driver):
        """
        En la tabla de resultados hace click en el ícono de descarga de la primera fila
        y retorna (filename, BytesIO, mimetype). Si falla: (None, None, None).
        """
        downloadDir = os.path.abspath("temp")
        self._enableDownloads(driver, downloadDir)

        # tabla lista
        waitVisible(driver, (By.CSS_SELECTOR, "table.cabecera-tabla tbody"))

        before = {f for f in os.listdir(downloadDir) if not f.endswith(".crdownload")}

        # ícono «Descargar XML» habilitado en la primera fila
        btnXml = waitClickable(
            driver,
            (By.XPATH, "//table[contains(@class,'cabecera-tabla')]//tbody//tr[1]"
                       "//i[contains(@class,'fa-download') and contains(@class,'icono') "
                       "and not(ancestor::span[contains(@class,'icono-disabled')])]"))
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

        try:
            os.remove(filePath)
        except Exception:
            pass

        return filename, BytesIO(data), mime
