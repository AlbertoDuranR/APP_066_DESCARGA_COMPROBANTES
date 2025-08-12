from utils.helpers import getDriver
from pages.loginPage import LoginPage
from pages.menuPage import MenuPage
from pages.formPage import FormPage
from pages.download import DownloadPage
import time

def main():
    driver = getDriver()
    try:
        LoginPage().login(driver)
        MenuPage().goToConsultaComprobantes(driver)
        FormPage().goToForm(driver)
        time.sleep(5)
        DownloadPage().downloadPDF(driver)
        
        print("✅ Navegación completada.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
