# pages/downloadPage.py
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.waits import waitVisible

class DownloadPage:
    def _switchToIframe(self, driver):
        # entra al iframe donde está el modal
        try:
            driver.switch_to.frame("iframeApplication")
        except Exception:
            iframe = waitVisible(driver, (By.ID, "iframeApplication"))
            driver.switch_to.frame(iframe)

    def downloadXML(self, driver, timeout=25):
        # --- forzar descargas a temp/ (Chrome/Chromium via CDP) ---
        download_dir = os.path.abspath("temp")
        os.makedirs(download_dir, exist_ok=True)
        
        try:
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": download_dir
            })
        except Exception:
            # si no soporta CDP, igual continuará con la config de Chrome por opciones
            pass

        self._switchToIframe(driver)

        # esperar a que el modal "Resultado" esté visible y sin spinner
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ngb-modal-window .modal-content"))
        )
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "ngx-spinner"))
        )

        # click en "Descargar XML"
        btnXml = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH, "//ngb-modal-window//button[@ngbtooltip='Descargar XML']"
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnXml)
        driver.execute_script("arguments[0].click();", btnXml)
