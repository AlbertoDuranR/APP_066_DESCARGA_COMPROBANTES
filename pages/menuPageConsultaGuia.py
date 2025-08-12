from selenium.webdriver.common.by import By
from utils.waits import waitClickable

class MenuPage:

    def goToGuiasRemision(self, driver):
        waitClickable(driver, (By.ID, "divOpcionServicio2")).click()
        waitClickable(driver, (By.ID, "nivel1_62")).click()
        waitClickable(driver, (By.CSS_SELECTOR, "li.opcionEmpresas[data-id='62.1']")).click()
        waitClickable(driver, (By.ID, "nivel3_62_1_5")).click()
        waitClickable(driver, (By.ID, "nivel4_62_1_5_1_1")).click()