import os
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

def getEnv(key):
    return os.getenv(key, "").strip()

def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)
