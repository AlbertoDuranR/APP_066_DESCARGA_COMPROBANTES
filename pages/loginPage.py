from selenium.webdriver.common.by import By
from utils.waits import waitVisible
from utils.helpers import getEnv

class LoginPage:
    def login(self, driver):
        url = getEnv("SUNAT_LOGIN_URL")
        ruc = getEnv("SUNAT_RUC")
        usuario = getEnv("SUNAT_USUARIO")
        password = getEnv("SUNAT_PASSWORD")

        driver.get(url)
        waitVisible(driver, (By.ID, "txtRuc")).send_keys(ruc)
        driver.find_element(By.ID, "txtUsuario").send_keys(usuario)
        driver.find_element(By.ID, "txtContrasena").send_keys(password)
        driver.find_element(By.ID, "btnAceptar").click()
