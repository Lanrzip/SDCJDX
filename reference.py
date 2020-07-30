from selenium.webdriver.chrome.options import Options
from splinter.browser import Browser
from browsermobproxy import Server
from time import sleep
from twilio.rest import Client

# 获取所有网络请求
server = Server("D:/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))


# disable-infobars
class HuoChe(object):
    """docstring for Train"""
    driver_name = 'Chrome'
    executable_path = 'D:\chromedriver.exe'
    # 用户名 密码
    username = u"20181754128"
    passwd = u"zxd123123"

    """网址"""
    # 我们学校强智选课URL
    select_url = "http://jw.sdufe.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=EDCD86DB92DC498FAB5C27AECA4117E5"
    # 强智登录URL
    login_url = "http://jw.sdufe.edu.cn/"
    initmy_url = "http://jw.sdufe.edu.cn/jsxsd/framework/xsMain.jsp"
    def __init__(self):
        print("Welcome To Use The Tool")

    # 登录模块
    def login(self):
        proxy.new_har()
        self.driver.visit(self.login_url)
        # 填充密码
        self.driver.fill("userAccount", self.username)
        # sleep(1)
        self.driver.fill("userPassword", self.passwd)
        print("等待验证码，自行输入....")
        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break

    # 抢课成功，利用twilio发送短信
    def send_message(self):
        account_sid = "your_sid"
        auth_token = "your_auth_totken"
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=u" 抢课成功，请登录查看 ", to="+8618653195606", from_="+15082515626")

    # 登录进入，开始抢课
    def start(self):
        self.driver = Browser(driver_name='chrome')
        self.driver.driver.set_window_size(1400, 1000)
        self.login()
        self.driver.visit(self.select_url)
        # 选择你想抢课的种类，名字或教学方式
        self.driver.find_by_text(u'公选课选课').click()
        class_name = u"智慧树"

        # 利用iframe表格找到想选的课的选课按钮，然后点击
        # 循环点击所有要抢的课的选课id，当抢课成功发送短信通知
        if self.driver.find_by_id('mainFrame'):
            with self.driver.get_iframe('mainFrame') as frame:
                b = frame.find_by_name("skls")
                b.fill(class_name)
                frame.find_by_value(u"查询").click()
                # 要抢课的id列表
                list = ['div_201920202009014','div_201920202009036','div_201920202009020','div_201920202009025','div_201920202009045','div_201920202009051','div_201920202009040']
                # 循环抢课，提示抢课成功后发送手机短信通知
                A = False
                while A == False:
                    for i in range(len(list)):
                        frame.find_by_id(list[i]).click()
                        with frame.get_alert() as alert:
                            alert.accept()
                            if alert.text == "选课失败：此课堂选课人数已满！":
                                alert.accept()
                                continue
                            elif alert.text == "选课成功":
                                alert.accept()
                                A = True
                                print('抢课成功')
                                self.send_message()
                                break
                            else:
                                alert.accept()
                                continue


if __name__ == "__main__":
    train = HuoChe()
    train.start()