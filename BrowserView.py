import pyotp
from flask import Flask, request
from time import sleep
from selenium import webdriver
from configparser import ConfigParser
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
config_object = ConfigParser()
config_object.read("config.ini")
userinfo = config_object["USERINFO"]

@app.route('/')
def home():
    return "App Works!!"

@app.route('/kitelogin')
def kitelogin():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(3)
    driver.get('https://kite.zerodha.com/')
    driver.find_element(By.XPATH, "//input[@id='userid']").send_keys(userinfo.get("userid"))
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(userinfo.get("password"))
    driver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()
    sleep(2)
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys(pyotp.TOTP(userinfo.get("totpkey")).now())
    sleep(1)
    driver.find_element(By.XPATH, "//button[@class='button button-blue']").click()
    enctoken = driver.get_cookie("enctoken")['value']
    return enctoken

if __name__ == '__main__':
     app.run()