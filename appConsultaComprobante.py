# from utils.helpers import getDriver
# from pages.loginPage import LoginPage
# from pages.menuPageConsultaComprobante import MenuPage
# from pages.formPageConsultaComprobante import FormPage
# from pages.downloadConsultaComprobante import DownloadPage
# import time

# def main():
#     driver = getDriver()
#     try:
#         rucEmisor = "20100055237"
#         serie = "F348"
#         correlativo = "99706"
#         LoginPage().login(driver)
#         MenuPage().goToConsultaComprobantes(driver)
#         FormPage().goToForm(driver, rucEmisor, serie, correlativo)
#         time.sleep(3)
#         DownloadPage().downloadXML(driver)
        
#         print("✅ Navegación completada.")
#     except Exception as e:
#         print(f"❌ Error: {e}")
#     finally:
#         time.sleep(5)
#         driver.quit()

# if __name__ == "__main__":
#     main()
