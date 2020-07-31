from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
import sys, time


USERNAME, PASSWORD, SEND_MESSAGE = '', '', ''
ACCOUNT, TOKEN, FROM, TO = '', '', '', ''
CATEGORY = ''


class XuankeSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生选课系统')
        self.status = self.statusBar()
        self.timer = QTimer()
        self.timer.start()
        self.timer.timeout.connect(self.show_time)

        layout = QGridLayout()

        """输入"""
        username_label = QLabel('用户名')
        self.username_line_edit = QLineEdit()
        username_label.setFont(QFont("Microsoft YaHei"))
        password_label = QLabel('密码')
        self.password_line_edit = QLineEdit()
        password_label.setFont(QFont("Microsoft YaHei"))

        self.username_line_edit.setPlaceholderText('请输入账号')
        self.password_line_edit.setPlaceholderText('请输入密码')


        # 限定11位整数
        int_validator = QRegExpValidator()
        reg = QRegExp(r'\d{11}')
        int_validator.setRegExp(reg)
        self.username_line_edit.setValidator(int_validator)
        # 输入密码时不显示
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        layout.addWidget(username_label, 1, 0, 1, 2)
        layout.addWidget(self.username_line_edit, 1, 2, 1, 2)
        layout.addWidget(password_label, 2, 0, 1, 2)
        layout.addWidget(self.password_line_edit, 2, 2, 1, 2)

        """选择"""
        self.check_message_box = QCheckBox('发送短信通知')
        self.check_message_box.stateChanged.connect(self.use_or_not)

        account_label = QLabel('account')
        account_label.setFont(QFont("Microsoft YaHei"))
        self.account_line_edit = QLineEdit()
        self.account_line_edit.setEnabled(False)
        token_label = QLabel('token')
        token_label.setFont(QFont("Microsoft YaHei"))
        self.token_line_edit = QLineEdit()
        self.token_line_edit.setEnabled(False)
        from_label = QLabel('from')
        from_label.setFont(QFont("Microsoft YaHei"))
        self.from_line_edit = QLineEdit()
        self.from_line_edit.setEnabled(False)
        to_label = QLabel('to')
        to_label.setFont(QFont("Microsoft YaHei"))
        self.to_line_edit = QLineEdit()
        self.to_line_edit.setEnabled(False)

        layout.addWidget(self.check_message_box, 3, 0, 1, 2)
        layout.addWidget(account_label, 4, 0, 1, 2)
        layout.addWidget(token_label, 5, 0, 1, 2)
        layout.addWidget(from_label, 6, 0, 1, 2)
        layout.addWidget(to_label, 7, 0, 1, 2)
        layout.addWidget(self.account_line_edit, 4, 2, 1, 2)
        layout.addWidget(self.token_line_edit, 5, 2, 1, 2)
        layout.addWidget(self.from_line_edit, 6, 2, 1, 2)
        layout.addWidget(self.to_line_edit, 7, 2, 1, 2)

        space_label = QLabel('')
        layout.addWidget(space_label, 8, 1, 1, 2)
        label = QLabel('选择选修课类型')
        layout.addWidget(label, 9, 0)
        self.category_button1 = QRadioButton('通识选修')
        self.category_button1.setChecked(True)
        self.category_button1.toggled.connect(self.category_state)
        self.category_button2 = QRadioButton('专业选修')
        self.category_button2.toggled.connect(self.category_state)
        layout.addWidget(self.category_button1, 10, 0)
        layout.addWidget(self.category_button2, 10, 1)

        label2 = QLabel('类别：')
        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(['所有课程','财经特色','传统文化','创新创业',
                                  '人文社科','自然科学','体育保健'])
        self.combo_box2 = QComboBox()
        self.combo_box2.addItems(['所有课程','...'])

        self.combo_box2.setEnabled(False)
        layout.addWidget(label2, 11, 0)
        layout.addWidget(self.combo_box1, 12, 0)
        layout.addWidget(self.combo_box2, 12, 1)

        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        """开始按钮"""
        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.validate)

        thread = MyThread()
        self.start_button.clicked.connect(lambda: thread.start())
        layout.addWidget(self.start_button, 18, 2)

        """终止按钮"""
        self.stop_button = QPushButton('终止')
        self.stop_button.clicked.connect(lambda: thread.terminate())
        layout.addWidget(self.stop_button, 18, 3)

        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(layout)

    def category_state(self):
        radio_button = self.sender()
        if radio_button.text() == '专业选修':
            self.combo_box1.setEnabled(False)
            self.combo_box2.setEnabled(True)
        elif radio_button.text() == '通识选修':
            self.combo_box1.setEnabled(True)
            self.combo_box2.setEnabled(False)
        else:
            pass

    def show_time(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.status.showMessage(timeDisplay)

    def use_or_not(self):
        check_box = self.sender()

        if check_box.isChecked():
            self.account_line_edit.setEnabled(True)
            self.token_line_edit.setEnabled(True)
            self.to_line_edit.setEnabled(True)
            self.from_line_edit.setEnabled(True)
            self.show_dialog()
        else:
            self.account_line_edit.setEnabled(False)
            self.token_line_edit.setEnabled(False)
            self.to_line_edit.setEnabled(False)
            self.from_line_edit.setEnabled(False)

    def show_dialog(self):
        message = "开启短信提醒功能请前往 <a href='https://www.twilio.com/'>twilio.com</a> 注册账号。 \
                  使用教程可参考 <a href=''>教程</a>, 会用当我没说。。。"
        reply = QMessageBox.information(self, '提示', message, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            self.check_message_box.setCheckState(0)
            
    def validate(self):
        global USERNAME, PASSWORD, SEND_MESSAGE, ACCOUNT, \
                TOKEN, FROM, TO, CATEGORY
        USERNAME = self.username_line_edit.text()
        PASSWORD = self.password_line_edit.text()

        ACCOUNT = self.account_line_edit.text()
        TOKEN = self.token_line_edit.text()
        FROM = self.from_line_edit.text()
        TO = self.to_line_edit.text()

        if self.category_button1.isChecked():
            CATEGORY = self.combo_box1.currentText()
        else:
            CATEGORY = self.combo_box2.currentText()


class MyThread(QThread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):

        print('开始')
        print(CATEGORY)
        driver_path = r'D:\eng\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get('http://jw.sdufe.edu.cn/')
        input_ID = driver.find_element_by_id('userAccount')
        input_PD = driver.find_element_by_id('userPassword')
        input_ID.send_keys(USERNAME)
        input_PD.send_keys(PASSWORD)

        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'maintext'))
        )

        iframe = driver.find_element_by_id('Frame0')
        driver.switch_to.frame(iframe)

        driver.find_element_by_xpath("//div[@class='panel-body']//div[@class='grid'][3]").click()



        """是否发送短信"""
        if ACCOUNT != '':
            self.send_message()

    def send_message(self):
        # ACCOUNT = "AC7f63698bf6c852f6311153fad0c9f941"
        # TOKEN = "fd4c30c60d30fa818fb428dd855023db"
        # FROM = '+18569421593'
        # TO = '+8618653195606'

        account = ACCOUNT
        token = TOKEN
        from_ = FROM
        to = TO

        client = Client(account, token)

        message = client.messages.create(to=to,
                                         from_=from_,
                                         body='抢课成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('timg.jpg'))
    qss = '''
QWidget
{
	background-color: #3a3a3a;
	color: #fff;
	selection-background-color: #b78620;
	selection-color: #000;

}
QLabel
{
	color: #b9b9bb;
	border-color: #000000;

}
QPushButton
{
	background-color: #ff9c2b;
	color: #000000;
	font-weight: bold;
	border-style: solid;
	border-color: #000000;
	padding: 6px;

}
QPushButton::hover
{
	background-color: rgba(183, 134, 32, 20%);
	border: 1px solid #b78620;

}

QPushButton::pressed
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));
	border: 1px solid #b78620;

}




QCheckBox
{
	background-color: transparent;
    color: lightgray;
	border: none;

}


QCheckBox::indicator
{
    background-color: #323232;
    border: 1px solid darkgray;
    width: 12px;
    height: 12px;

}


QCheckBox::indicator:checked
{
    image:url("./check_mark.png");
	background-color: #b78620;
    border: 1px solid #3a546e;

}
QCheckBox::indicator:unchecked:hover
{
	border: 1px solid #b78620; 

}


QRadioButton 
{
	color: #fff;
	background-color: transparent;

}


QRadioButton::indicator::unchecked:hover 
{
	background-color: #d3d3d3;
	border: 2px solid #002b2b;
	border-radius: 6px;
}


QRadioButton::indicator::checked 
{
	border: 2px solid #52beff;
	border-radius: 6px;
	background-color: #002b2b;  
	width: 9px; 
	height: 9px; 

}
QComboBox
{
    background-color: #4a5157;
    padding-left: 6px;
    color: #fff;
    height: 20px;
	border-radius: 4px;

}


QComboBox::disabled
{
	background-color: #404040;
	color: #656565;
	border-color: #051a39;

}


QComboBox:on
{
    background-color: #4a5157;
	color: #fff;

}


QComboBox QAbstractItemView
{
    background-color: #4a5157;
    color: #fff;
    selection-background-color: #002b2b;
	selection-color: #fff;
    outline: 0;

}


QComboBox::drop-down
{
	background-color: #4a5157;
    subcontrol-origin: padding;
    subcontrol-position: top right;
	border-radius: 4px;
    width: 15px;

}


QComboBox::down-arrow
{
    image: url(./arrow_down.png);
    width: 8px;
    height: 8px;

}



QLineEdit{
	background-color: #4d4d4d;
	color: #fff;
	font-weight: bold;
	border-style: solid;
	border-radius: 5px;
	padding: 5px;

}



    '''
    app.setStyleSheet(qss)
    main = XuankeSystem()
    main.show()

    sys.exit(app.exec_())
