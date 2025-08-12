from utils.waits import waitVisible, waitClickable
from selenium.webdriver.common.by import By
import os


class DownloadPage:
    def downloadXML(self, driver):
        # 0) Forzar descargas a ./temp
        download_dir = os.path.abspath("temp")
        os.makedirs(download_dir, exist_ok=True)
        try:
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": download_dir
            })
        except Exception:
            pass  # si no soporta CDP, seguirá con la config por defecto

        # 6) Esperar la tabla
        waitVisible(driver, (By.CSS_SELECTOR, "table.cabecera-tabla tbody"))

        # 7) Click en "Descargar XML" (ícono activo, no disabled) de la primera fila
        btnXml = waitClickable(
            driver,
            (By.XPATH, "//table[contains(@class,'cabecera-tabla')]//tbody//tr[1]"
                    "//i[contains(@class,'fa-download') and contains(@class,'icono') "
                    "and not(ancestor::span[contains(@class,'icono-disabled')])]"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnXml)
        driver.execute_script("arguments[0].click();", btnXml)