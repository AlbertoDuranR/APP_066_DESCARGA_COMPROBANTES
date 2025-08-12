from utils.helpers import getDriver
from pages.loginPage import LoginPage
from pages.menuPageConsultaGuia import MenuPage
from pages.formPageConsultaGuia import FormPage
import time

def main():
    driver = getDriver()
    try:
        LoginPage().login(driver)
        MenuPage().goToGuiasRemision(driver)
        time.sleep(5)
        FormPage().goToForm(driver)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
