import time
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.support.ui import Select
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
    bid = ''
    class_list = []

    def __init__(self):
        super().__init__()

    def run(self):
        print('开始')
        print(self.category)
        
        url = f"http://jw.sdufe.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid={self.bid}"

        driver_path = r'D:\eng\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get('http://jw.sdufe.edu.cn/')
        input_id = driver.find_element_by_id('userAccount')
        input_pd = driver.find_element_by_id('userPassword')
        input_id.send_keys(self.username)
        input_pd.send_keys(self.password)

        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'maintext'))
        )

        driver.get(url)

        driver.find_element_by_xpath("//*[contains(text(), '公选课选课')]").click()
        driver.execute_script("window.open('http://jw.sdufe.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk')")
        driver.switch_to.window(driver.window_handles[1])
        selectTag = Select(driver.find_element_by_name('szjylb'))
        selectTag.select_by_visible_text(self.category)
        teacher = driver.find_element_by_id('skls')
        teacher.send_keys('智慧树')
        driver.find_element_by_xpath(".//input[@type='button']").click()
        time.sleep(0.5)
        class_list = self.class_list
        for cla in class_list:
            select = driver.find_element_by_xpath(f"//td[contains(text(), '{cla}')]/../td[last()]/div").click()
            alert = driver.switch_to.alert
            alert.accept()
            if alert.text == "选课失败：此课堂选课人数已满！":
                alert.accept()
                continue
            elif alert.text == "选课成功":
                alert.accept()
                if self.account != '':
                    self.send_message()
                break
            else:
                try:
                    alert.accept()
                    break
                except:
                    break

    def send_message(self):
        # ACCOUNT = "AC7f63698bf6c852f6311153fad0c9f941"
        # TOKEN = "74e63b4efb4a4fb4df4303f2fd49cd2d"
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


