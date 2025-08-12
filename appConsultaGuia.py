# from utils.helpers import getDriver
# from pages.loginPage import LoginPage
# from pages.menuPageConsultaGuia import MenuPage
# from pages.formPageConsultaGuia import FormPage
# from pages.downloadConsultaGuia import DownloadPage
# import time

# def main():
#     driver = getDriver()
#     try:
#         serie = "T100"
#         numero = "94565"
#         LoginPage().login(driver)
#         MenuPage().goToGuiasRemision(driver)
#         time.sleep(5)
#         FormPage().goToForm(driver, serie, numero)
#         DownloadPage().downloadXML(driver)

#     except Exception as e:
#         print(f"❌ Error: {e}")
#     finally:
#         time.sleep(5)
#         driver.quit()

# if __name__ == "__main__":
#     main()
