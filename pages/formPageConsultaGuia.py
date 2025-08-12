from utils.waits import waitVisible, waitClickable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

class FormPage:
    def goToForm(self, driver, serie, numero):

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

        # 1) Seleccione el tipo de GRE (clic al label para evitar input oculto)
        lblTipo = waitClickable(driver, (By.CSS_SELECTOR, f"label.form-check-label[for='09']"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", lblTipo)
        driver.execute_script("arguments[0].click();", lblTipo)

        # 2) RUC del emisor
        rucEmisor = "20100055237"
        inpRuc = waitVisible(driver, (By.CSS_SELECTOR, "input#rucEmisor[formcontrolname='rucEmisor']"))
        inpRuc.clear(); inpRuc.send_keys(rucEmisor); inpRuc.send_keys(Keys.TAB)

        # 3) Serie
        serie = "T100"
        inpSerie = waitVisible(driver, (By.CSS_SELECTOR, "input[formcontrolname='serie']"))
        inpSerie.clear(); inpSerie.send_keys(serie); inpSerie.send_keys(Keys.TAB)

        # 4) Número
        numero = "94565"
        inpNumero = waitVisible(driver, (By.CSS_SELECTOR, "input[formcontrolname='numero']"))
        inpNumero.clear(); inpNumero.send_keys(numero); inpNumero.send_keys(Keys.TAB)

        # 5) Click en Siguiente (espera a que se habilite)
        btnSiguiente = waitClickable(driver, (By.CSS_SELECTOR, "button[type='submit']:not([disabled])"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnSiguiente)
        driver.execute_script("arguments[0].click();", btnSiguiente)

        