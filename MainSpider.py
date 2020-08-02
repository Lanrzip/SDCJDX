from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MyThread(QThread):
    username, password = '', ''
    account, token, from_, to = '', '', '', ''
    category = ''
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):

        print('开始')
        print(self.category)
        driver_path = r'D:\eng\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get('http://jw.sdufe.edu.cn/')
        input_ID = driver.find_element_by_id('userAccount')
        input_PD = driver.find_element_by_id('userPassword')
        input_ID.send_keys(self.username)
        input_PD.send_keys(self.password)

        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'maintext'))
        )

        iframe = driver.find_element_by_id('Frame0')
        driver.switch_to.frame(iframe)

        driver.find_element_by_xpath("//div[@class='panel-body']//div[@class='grid'][3]").click()



        """是否发送短信"""
        if self.account != '':
            self.send_message()

    def send_message(self):
        # ACCOUNT = "AC7f63698bf6c852f6311153fad0c9f941"
        # TOKEN = "fd4c30c60d30fa818fb428dd855023db"
        # FROM = '+18569421593'
        # TO = '+8618653195606'

        account = self.account
        token = self.token
        from_ = self.from_
        to = self.to

        client = Client(account, token)

        message = client.messages.create(to=to,
                                         from_=from_,
                                         body='抢课成功')


