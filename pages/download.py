# pages/downloadPage.py
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

    def downloadPDF(self, driver, timeout=25):
        self._switchToIframe(driver)

        # esperar a que el modal "Resultado" esté visible y sin spinner
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ngb-modal-window .modal-content"))
        )
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "ngx-spinner"))
        )

        # click en "Descargar PDF"
        btnPdf = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH, "//ngb-modal-window//button[@ngbtooltip='Descargar PDF']"
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnPdf)
        driver.execute_script("arguments[0].click();", btnPdf)
