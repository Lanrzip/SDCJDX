from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class XuankeSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生选课系统')
        self.resize(800,600)

        form_layout = QFormLayout()

        """输入"""
        self.username_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()

        self.username_line_edit.setPlaceholderText('请输入账号')
        self.password_line_edit.setPlaceholderText('请输入密码')

        # 限定11位整数
        int_validator = QRegExpValidator()
        reg = QRegExp(r'\d{11}')
        int_validator.setRegExp(reg)
        self.username_line_edit.setValidator(int_validator)
        # 输入密码时不显示
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        form_layout.addRow('用户名', self.username_line_edit)
        form_layout.addRow('密码', self.password_line_edit)

        """选择"""
        self.check_message_box = QCheckBox('发送短信通知')
        self.check_message_box.stateChanged.connect(self.use_or_not)

        self.account_line_edit = QLineEdit()
        self.account_line_edit.setEnabled(False)
        self.token_line_edit = QLineEdit()
        self.token_line_edit.setEnabled(False)
        self.from_line_edit = QLineEdit()
        self.from_line_edit.setEnabled(False)
        self.to_line_edit = QLineEdit()
        self.to_line_edit.setEnabled(False)


        form_layout.addRow('', self.check_message_box)
        form_layout.addRow('account', self.account_line_edit)
        form_layout.addRow('token', self.token_line_edit)
        form_layout.addRow('from', self.from_line_edit)
        form_layout.addRow('to', self.to_line_edit)

        """开始按钮"""
        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.login)

        form_layout.addRow(self.start_button)

        self.setLayout(form_layout)

    def use_or_not(self):
        check_box = self.sender()

        if check_box.isChecked():
            self.account_line_edit.setEnabled(True)
            self.token_line_edit.setEnabled(True)
            self.to_line_edit.setEnabled(True)
            self.from_line_edit.setEnabled(True)
        else:
            self.account_line_edit.setEnabled(False)
            self.token_line_edit.setEnabled(False)
            self.to_line_edit.setEnabled(False)
            self.from_line_edit.setEnabled(False)

    def login(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        print('开始')
        print(self.check_message_box.isChecked())

        driver_path = r'D:\eng\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get('http://jw.sdufe.edu.cn/')
        input_ID = driver.find_element_by_id('userAccount')
        input_PD = driver.find_element_by_id('userPassword')
        input_ID.send_keys(username)
        input_PD.send_keys(password)

        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'maintext'))
        )

        iframe = driver.find_element_by_id('Frame0')
        driver.switch_to.frame(iframe)

        driver.find_element_by_xpath("//div[@class='panel-body']//div[@class='grid'][3]").click()


        """是否发送短信"""
        if self.account_line_edit.text() != '':
            self.send_message()

    def send_message(self):
        ACCOUNT = "AC7f63698bf6c852f6311153fad0c9f941"
        TOKEN = "fd4c30c60d30fa818fb428dd855023db"
        FROM = '+18569421593'
        TO = '+8618653195606'


        account = self.account_line_edit.text()
        token = self.token_line_edit.text()
        from_ = self.from_line_edit.text()
        to = self.to_line_edit.text()

        client = Client(account, token)

        message = client.messages.create(to=to,
                                         from_=from_,
                                         body='抢课成功')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = XuankeSystem()
    main.show()

    sys.exit(app.exec_())