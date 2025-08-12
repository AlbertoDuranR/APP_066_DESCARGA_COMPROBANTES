from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def waitClickable(driver, locator, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

def waitVisible(driver, locator, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
