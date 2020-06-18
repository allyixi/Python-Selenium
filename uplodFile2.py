# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import win32gui
import win32con
import requests
# import public.public_parm as public_parm
import time


class UploadFile():
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')  # 设置option
    option.add_argument('-start-maximized')
    driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器

    # driver = webdriver.Chrome()
    ip = "192.168.4.46"
    port = "8310"
    cookieValue = ''
    user = "test"
    psd = "icenter"

    def __init__(self, ip, port, uesrName, password):
        self.ip = ip
        self.port = port
        self.user = uesrName
        self.psd = password

    def upload(self, params, startTime):
        self.driver.get("http://"+self.ip+":"+self.port)
        # 免密码登录
        # self.driver.maximize_window()
        # self.driver.delete_all_cookies()
        # cookie = {'domain': self.ip, 'httpOnly': False, 'name': 'Authorization', 'path': '/', 'secure': False, 'value': self.cookieValue }
        # self.driver.add_cookie(cookie)
        # self.driver.refresh()
        # 登录
        time.sleep(5)
        loginForms = self.driver.find_elements_by_class_name("login-form-panel")
        loginForm = ""
        for item in loginForms:
            if item.is_displayed():
                loginForm = item
        userNameInput = loginForm.find_elements_by_class_name("el-input__inner")
        for item in userNameInput:
            if "请输入用户名" == item.get_property("placeholder"):
                item.clear()
                item.send_keys(self.user)
            elif "请输入密码" == item.get_property("placeholder"):
                item.send_keys(self.psd)
        loginButton = loginForm.find_element_by_tag_name("button")
        loginButton.click()
        time.sleep(5)
        #进入数据管理页面
        mainPage = None
        time.sleep(5)
        for waitTime in range(0, 10):
            try:
                mainPage = self.driver.find_element_by_class_name("full-container")
                break
            except NoSuchElementException:
                time.sleep(1)
        if not mainPage:
            self.driver.quit()
            return
        navwrap = self.driver.find_element_by_class_name("nav-wrap")
        menuList = navwrap.find_elements_by_tag_name("a")
        chengedPage = False
        for menu in menuList:
            if "数据管理" == menu.text:
                menu.click()
                chengedPage = True
                time.sleep(3)
                break
        if not chengedPage:
            print("未找到数据管理菜单")
            self.driver.quit()
            return
        # 选择要上传到的文件夹
        folderFilterTree = None
        for waitTime in range(0,10):
            try:
                folderFilterTree = self.driver.find_element_by_id("filterTree")
                break
            except NoSuchElementException:
                time.sleep(1)
        # 点击上传
        operbtns =self.driver.find_element_by_class_name("oper-btns")
        uploadButton = operbtns.find_element_by_class_name("el-dropdown")
        for param in params:
            respons = requests.request(method="GET", url="http://192.168.4.46:8310/user/jwt/time")
            while int(startTime) > int(respons.text):
                respons = requests.request(method="GET", url="http://192.168.4.46:8310/user/jwt/time")
                if int(startTime) == int(respons.text):
                    break
            uploadButton.click()
            for i in range(0, 5):
                time.sleep(2)
                try:
                    dropdownmenu = self.driver.find_elements_by_class_name("el-dropdown-menu")
                    liList = dropdownmenu[len(dropdownmenu)-1].find_elements_by_tag_name("li")
                    findTagFileType = False
                    for li in liList:
                        if param["fileType"] == li.get_property("title"):
                            li.click()
                            findTagFileType = True
                            break
                    if findTagFileType:
                        time.sleep(3)
                        dialog = win32gui.FindWindow('#32770', u'打开')  # 找到windows对话框参数是（className，title）
                        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
                        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
                        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)
                        # 上面3句依次找对象，直到找出输入框Edit对象的句柄
                        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮
                        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, 0, param["filepath"])
                        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
                        time.sleep(5)
                        break
                    else:
                        print("未找到【"+param["fileType"]+"】类型文件上传按钮")
                        break
                except NoSuchElementException:
                    print("未找到【" + param["fileType"] + "】类型文件上传按钮1")
                    time.sleep(1)
            uploadButton.click()
        # dropdownElements = self.driver.find_elements_by_class_name("el-dropdown")
        # for dropdown in dropdownElements:
        #     if self.user == dropdown.text:
        #         dropdown.click()
        #         break
        # time.sleep(1)
        # self.driver.find_element_by_class_name("fa-sign-out").click()
        # time.sleep(1)
        # self.driver.delete_all_cookies()
        # self.driver.quit()

from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
def openChrome(url):
    driver = webdriver.Chrome()
    driver.get(url)


if __name__ == '__main__':
    t = [{"fileType": "原始影像", "filepath": "C:\\Users\\admin\\Desktop\\GF3_MDJ_NSC_009498_E121.2_N34.1_20180530_L1A_HHHV_L10003226453.tar.gz"},
        # {"fileType": "成果影像", "filepath": "\\\\192.168.49.40\\测试部共享\\测试数据\\iCenter1.1\\maoyanData\\其它数据\\成果影像\\ImageMosic.tiff"},
        # {"fileType": "矢量", "filepath": "\\\\192.168.49.40\\测试部共享\\测试数据\\iCenter1.1\\maoyanData\\其它数据\\矢量\\prov.zip"},
        # {"fileType": "地形", "filepath": "\\\\192.168.49.40\\测试部共享\\测试数据\\iCenter1.1\\maoyanData\\其它数据\\地形\\GlobalDEM1Km.tif"},
        # {"fileType": "文档", "filepath": "\\\\192.168.49.40\\测试部共享\\测试数据\\iCenter1.1\\maoyanData\\其它数据\\图片\\ISO9126.png"},
        # {"fileType": "图片", "filepath": "\\\\192.168.49.40\\测试部共享\\测试数据\\iCenter1.1\\maoyanData\\其它数据\\文档\\gvml.config.json"},
        ]
    uploadFile = UploadFile("192.168.4.46", "8310", "test", "icenter")
    uploadFile.upload(t,"20200110070830")
    # data = ["http://192.168.4.37:8310",
    #         "http://192.168.4.211:8310"]
    # token = public_parm.get_token("http://192.168.4.37:8310", "baibo", "123456")
    #     wait(all_task, return_when=ALL_COMPLETED)
    # with ThreadPoolExecutor(max_workers=len(data)) as executor:
    #     all_task = [executor.submit(openChrome, param) for param in data]
    #     wait(all_task, return_when=ALL_COMPLETED)
    # threads = []
    # for url in data:
    #     # 多线程
    #     t1 = threading.Thread(target=openChrome, args=(url,))
    #     threads.append(t1)
    # # 启动
    # for t2 in threads:
    #     t2.start()
    #     t2.join()  # 此处注释掉会同时运行。但同时运行可能会出现遮挡导致有问题哦。
