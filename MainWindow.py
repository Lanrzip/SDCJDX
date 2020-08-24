import sys, time, re
from MainSpider import *
from PoemSpider import *
from TitleBar import *


class XuankeSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        # 窗口置顶 | 不显示标题栏
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生选课系统')
        self.setFixedSize(840,480)
        # 状态栏显示时间
        self.status = self.statusBar()
        self.status.setObjectName('DownWidget')
        self.timer = QTimer()
        self.timer.start()
        self.timer.timeout.connect(self.show_time)

        """输入"""
        username_label = QLabel('用户名')
        username_label.setFont(QFont("Microsoft YaHei"))
        username_label.setObjectName('Label')

        password_label = QLabel('密码')
        password_label.setFont(QFont("Microsoft YaHei"))
        password_label.setObjectName('Label')

        zbid_label = QLabel('BID')
        zbid_label.setFont(QFont("Microsoft YaHei"))
        zbid_label.setObjectName('Label')

        self.username_line_edit = QLineEdit()
        self.username_line_edit.setPlaceholderText('请输入学号')
        self.username_line_edit.setObjectName('Edit')
        # 限定11位整数
        int_validator = QRegExpValidator()
        reg = QRegExp(r'\d{11}')
        int_validator.setRegExp(reg)
        self.username_line_edit.setValidator(int_validator)

        self.password_line_edit = QLineEdit()
        self.password_line_edit.setPlaceholderText('请输入密码')
        self.password_line_edit.setObjectName('Edit')
        # 输入密码时不显示
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        self.zbid_line_edit = QLineEdit()
        self.zbid_line_edit.setPlaceholderText('此项必填')
        self.zbid_line_edit.setObjectName('Edit')


        """选择"""
        self.check_message_box = QCheckBox('发送短信通知')
        self.check_message_box.stateChanged.connect(self.use_or_not)

        account_label = QLabel('ACCOUNT')
        token_label = QLabel('TOKEN')
        from_label = QLabel('FROM')
        to_label = QLabel('TO')

        account_label.setFont(QFont("Microsoft YaHei"))
        token_label.setFont(QFont("Microsoft YaHei"))
        from_label.setFont(QFont("Microsoft YaHei"))
        to_label.setFont(QFont("Microsoft YaHei"))

        account_label.setObjectName('Label')
        token_label.setObjectName('Label')
        from_label.setObjectName('Label')
        to_label.setObjectName('Label')

        self.account_line_edit = QLineEdit()
        self.token_line_edit = QLineEdit()
        self.from_line_edit = QLineEdit()
        self.to_line_edit = QLineEdit()
        self.account_line_edit.setObjectName('rEdit')
        self.token_line_edit.setObjectName('rEdit')
        self.from_line_edit.setObjectName('rEdit')
        self.to_line_edit.setObjectName('rEdit')
        self.account_line_edit.setEnabled(False)
        self.token_line_edit.setEnabled(False)
        self.from_line_edit.setEnabled(False)
        self.to_line_edit.setEnabled(False)

        space_label = QLabel('')
        label = QLabel('选择通识选修课类别')
        label.setObjectName('Label')

        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(['所有课程','传统文化类','创新创业类',
                                  '人文社科类','自然科学类','体育保健类'])

        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        """开始按钮"""
        self.start_button = QPushButton('开始')
        self.start_button.setObjectName('Button')
        """终止按钮"""
        self.stop_button = QPushButton('终止')
        self.stop_button.setObjectName('Button')

        """选课主线程"""
        thread = MyThread()
        self.start_button.clicked.connect(lambda: self.validate(thread))
        self.start_button.clicked.connect(lambda: thread.start())
        self.stop_button.clicked.connect(lambda: thread.terminate())

        down_left_layout = QGridLayout()

        down_left_layout.addWidget(username_label, 0, 0, 1, 2)
        down_left_layout.addWidget(password_label, 1, 0, 1, 2)
        down_left_layout.addWidget(self.username_line_edit, 0, 2, 1, 2)
        down_left_layout.addWidget(self.password_line_edit, 1, 2, 1, 2)
        down_left_layout.addWidget(zbid_label, 2, 0, 1, 2)
        down_left_layout.addWidget(self.zbid_line_edit, 2, 2, 1, 2)
        down_left_layout.addWidget(self.check_message_box, 3, 0, 1, 2)
        down_left_layout.addWidget(account_label, 4, 0, 1, 2)
        down_left_layout.addWidget(token_label, 5, 0, 1, 2)
        down_left_layout.addWidget(from_label, 6, 0, 1, 2)
        down_left_layout.addWidget(to_label, 7, 0, 1, 2)
        down_left_layout.addWidget(self.account_line_edit, 4, 2, 1, 2)
        down_left_layout.addWidget(self.token_line_edit, 5, 2, 1, 2)
        down_left_layout.addWidget(self.from_line_edit, 6, 2, 1, 2)
        down_left_layout.addWidget(self.to_line_edit, 7, 2, 1, 2)
        down_left_layout.addWidget(space_label, 8, 1, 1, 2)
        down_left_layout.addWidget(label, 9, 0)
        down_left_layout.addWidget(self.combo_box1, 12, 0)
        down_left_layout.addWidget(self.start_button, 18, 2)
        down_left_layout.addWidget(self.stop_button, 18, 3)

        self.titleBar = TitleBar(self)
        self.titleBar.set_title('学生选课系统')
        self.titleBar.setObjectName('UpWidget')
        up_layout = QVBoxLayout()
        up_layout.addWidget(self.titleBar)
        up_layout.setContentsMargins(0, 0, 0, 0)

        up_widget = QWidget()
        up_widget.setObjectName('UpWidget')
        up_widget.setLayout(up_layout)

        down_widget = QWidget()
        down_widget.setObjectName('DownWidget')

        down_left_widget = QWidget()
        down_left_widget.setLayout(down_left_layout)

        down_right_widget = QWidget()
        down_right_layout = QGridLayout()
        self.poem_button = QPushButton('好诗好诗')
        self.poem_button.setObjectName('poem')
        self.poem_text_edit = QPlainTextEdit()

        poem_thread = PoemThread()
        poem_thread.poem_signal.connect(self.show_poem)
        self.poem_button.clicked.connect(lambda: poem_thread.start())

        down_right_layout.addWidget(self.poem_text_edit, 0, 0, 1 ,2 )
        down_right_layout.addWidget(self.poem_button, 1, 1, 1, 1)

        down_right_widget.setLayout(down_right_layout)

        self.down_center_edit = QPlainTextEdit()
        self.down_center_edit.setPlaceholderText("填入同一类别的课程编号，以空格分隔。例： \n"
                                                 "411WK047 411WK049 411WK046")

        down_center_widget = QWidget()
        down_center_layout = QVBoxLayout()
        down_center_layout.addWidget(self.down_center_edit)
        down_center_widget.setLayout(down_center_layout)

        down_layout = QHBoxLayout()
        down_layout.addWidget(down_left_widget)
        down_layout.addWidget(down_center_widget)
        down_layout.addWidget(down_right_widget)

        down_widget.setLayout(down_layout)

        global_layout = QVBoxLayout()
        global_layout.addWidget(up_widget)
        global_layout.addWidget(down_widget)
        global_layout.setStretch(1, 10)
        global_layout.setSpacing(0)
        global_layout.setContentsMargins(0, 0, 0, 0)

        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(global_layout)

    """显示诗句"""
    def show_poem(self, poem):
        self.poem_text_edit.setPlainText(poem)
        self.poem_button.setText('换一首')

    """状态栏显示时间"""
    def show_time(self):
        time_ = QDateTime.currentDateTime()
        time_display = time_.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.status.showMessage(time_display)

    """是否使用短信功能"""
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

    """开启短信功能提示对话框"""
    def show_dialog(self):
        message = "开启短信提醒功能请前往 <a href='https://www.twilio.com/'>twilio.com</a> 注册账号。 \
                  使用教程可参考 <a href='https://blog.csdn.net/ddjhpxs/article/details/107692185'>注册教程</a>, 会用当我没说。。。"
        reply = QMessageBox.information(self, '提示', message, QMessageBox.Yes | QMessageBox.No)
        self.setObjectName('DownWidget')
        if reply == QMessageBox.No:
            self.check_message_box.setCheckState(0)

    """校验"""
    def validate(self, thread):
        thread.username = self.username_line_edit.text()
        thread.password = self.password_line_edit.text()
        thread.bid = self.zbid_line_edit.text()

        thread.account = self.account_line_edit.text()
        thread.token = self.token_line_edit.text()
        thread.from_ = self.from_line_edit.text()
        thread.to = self.to_line_edit.text()

        thread.category = self.combo_box1.currentText()

        text = self.down_center_edit.toPlainText().replace("\n", " ")
        text = re.sub(r"\s+", ',', text)
        print(text)
        thread.class_list = text.split(",")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle('Fusion')
    app.setWindowIcon(QIcon('res/crap.png'))

    with open('res/preset.qss', 'r', encoding='utf-8') as fp:
        qss = fp.read()
        app.setStyleSheet(qss)

    main = XuankeSystem()
    main.show()

    sys.exit(app.exec_())
