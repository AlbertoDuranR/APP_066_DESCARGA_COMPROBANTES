from utils.waits import waitVisible, waitClickable
from selenium.webdriver.common.by import By

class FormPage:
    def goToForm(self, driver):

        # 0) entrar al iframe
        iframe = waitVisible(driver, (By.ID, "iframeApplication"))
        driver.switch_to.frame(iframe)

        # Datos iniciales

        # 1) click en "GRE recibidas"
        btn_recibidas = waitClickable(driver, (By.XPATH, "//button[normalize-space()='GRE recibidas']"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_recibidas)
        driver.execute_script("arguments[0].click();", btn_recibidas)

        # 2) click en "Siguiente"
        btn_siguiente = waitClickable(driver, (By.XPATH, "//button[normalize-space()='Siguiente']"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_siguiente)
        driver.execute_script("arguments[0].click();", btn_siguiente)

        # 2. Criterios de búsqueda
        