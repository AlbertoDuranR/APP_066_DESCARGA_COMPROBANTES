from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.waits import waitVisible, waitClickable
from selenium.webdriver.common.keys import Keys
import time

class FormPage:
    def goToForm(self, driver, rucEmisor, serie, correlativo):
        # 0) entrar al iframe
        iframe = waitVisible(driver, (By.ID, "iframeApplication"))
        driver.switch_to.frame(iframe)

        # (opcional) esperar a que desaparezca el spinner de Angular
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "ngx-spinner"))
        )


        # 1) seleccionar filtro (clic al LABEL, luego verificamos el input)
        label = waitClickable(driver, (By.CSS_SELECTOR, f"label.custom-control-label[for='recibido']"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
        driver.execute_script("arguments[0].click();", label)

        time.sleep(3)

        # 2) RUC Emisor (robusto)
        # 2.1 evento tab
        rucInp = waitVisible(driver, (By.CSS_SELECTOR, "input[formcontrolname='rucEmisor']"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rucInp)
        rucInp.clear()
        rucInp.send_keys(rucEmisor)
        rucInp.send_keys(Keys.TAB)


        # 3) Tipo de comprobante (dropdown PrimeNG)
        time.sleep(3)
        dd = waitClickable(driver, (By.CSS_SELECTOR, "p-dropdown[formcontrolname='tipoComprobanteI'] .p-dropdown"))
        driver.execute_script("arguments[0].click();", dd)
        opcion = waitClickable(
            driver,
            (By.XPATH, f"//li[@role='option']//span[normalize-space()='Factura']/ancestor::li")
        )
        driver.execute_script("arguments[0].click();", opcion)


        # 4) Serie
        time.sleep(2)
        serie_inp = waitVisible(driver, (By.CSS_SELECTOR, "input[formcontrolname='serieComprobante']"))
        serie_inp.clear()
        serie_inp.send_keys(serie)



        # 5) Número de comprobante
        time.sleep(1)
        correlativo_inp = waitVisible(driver, (By.CSS_SELECTOR, "input[formcontrolname='numeroComprobante']"))
        correlativo_inp.clear()
        correlativo_inp.send_keys(correlativo)

        # Click en botón Consultar
        time.sleep(2)
        btnConsultar = waitClickable(driver, (By.XPATH, "//button[contains(., 'Consultar')]"))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnConsultar)
        driver.execute_script("arguments[0].click();", btnConsultar)

        driver.switch_to.default_content()




