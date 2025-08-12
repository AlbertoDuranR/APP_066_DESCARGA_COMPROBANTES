from selenium.webdriver.common.by import By
from utils.waits import waitClickable

class MenuPage:

    def goToConsultaComprobantes(self, driver):
        waitClickable(driver, (By.ID, "divOpcionServicio2")).click()
        waitClickable(driver, (By.ID, "nivel1_11")).click()
        waitClickable(driver, (By.ID, "nivel2_11_38")).click()
        waitClickable(driver, (By.ID, "nivel3_11_38_1")).click()
        waitClickable(driver, (By.ID, "nivel4_11_38_1_1_1")).click()
