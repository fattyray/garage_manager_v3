# -*- coding: utf-8 -*-
import json
import time
# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.7

from threading import Thread
from time import sleep, ctime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

import get_img
import asyncio
import getmask
import ocr


class Ui_MainWindow(object):
    def __init__(self):
        self.carplate = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1058, 752)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
        #centralwidget{  
        background-image: url('background.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        }
                     

               """)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(820, 70, 314, 621))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.right_inputs = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.right_inputs.setContentsMargins(0, 0, 0, 0)
        self.right_inputs.setObjectName("right_inputs")
        self.btn_loop = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.btn_loop.setObjectName("btn_loop")
        self.right_inputs.addWidget(self.btn_loop)
        self.btn_detect = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.btn_detect.setObjectName("btn_detect")
        self.right_inputs.addWidget(self.btn_detect)
        self.btns = QtWidgets.QVBoxLayout()
        self.btns.setObjectName("btns")
        self.btn2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn2.setObjectName("btn2")
        self.btns.addWidget(self.btn2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)
        self.btns.addLayout(self.verticalLayout)
        self.right_inputs.addLayout(self.btns)
        self.admin = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.admin.setObjectName("admin")
        self.right_inputs.addWidget(self.admin)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.right_inputs.addWidget(self.commandLinkButton)
        self.event_box = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.event_box.setGeometry(QtCore.QRect(30, 550, 751, 151))
        self.event_box.setPlainText("")
        self.event_box.setObjectName("event_box")
        self.cam_pic = QtWidgets.QLabel(self.centralwidget)
        self.cam_pic.setGeometry(QtCore.QRect(0, 0, 811, 321))
        self.cam_pic.setIndent(1)
        self.cam_pic.setObjectName("cam_pic")
        self.chepai_pic = QtWidgets.QLabel(self.centralwidget)
        self.chepai_pic.setGeometry(QtCore.QRect(10, 360, 811, 181))
        self.chepai_pic.setObjectName("chepai_pic")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1058, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        ui.checkBox_2.clicked.connect(autopay)
        ui.checkBox_3.clicked.connect(autoscan)
        ui.btn_detect.clicked.connect(detect_once)
        ui.btn_loop.clicked.connect(detect_loop)
        ui.admin.clicked.connect(self.openadmin)
        ui.commandLinkButton.clicked.connect(self.pay)
        self.btn2.clicked.connect(self.inout)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.carplate = ''
    def openadmin(self):
        import adminpage
        self.p1=adminpage.Ui_MainWindow()
        self.p1.show()

    def pay(self):
        import pay
        self.p2=pay.Ui_MainWindow()
        self.p2.show()

    def inout(self):
        import inout
        print("cp:",self.carplate)
        sss=''
        ori_data = {"cap": False, "plate": None,"info":None}
        with open("carinfo.json","w")as cinfo:
            json.dump(ori_data,cinfo)
        if inout.isfull(1):
            self.event_box.setPlainText("车库已经满了")
            return

        if len(self.carplate)==0:
            self.event_box.setPlainText("你还没有进行车牌的识别呢")
            return
        else:
            ori_data["cap"]=True
            ori_data["plate"]=self.carplate
            ori_data["info"] = "请注册账号并验证非超长超高后可使用"
            with open("carinfo.json", "w") as cinfo:
                json.dump(ori_data, cinfo)
            print(self.carplate)
        if not inout.CanEnter(self.carplate):
            self.event_box.setPlainText("您的车牌尚未注册或者是过长过高的车型（不支持入内）")
            import sign_up
            self.ss = sign_up.Ui_MainWindow()
            self.ss.show()
            return
        else:
            sss+="正在处理中，请稍后\n"
            if inout.isin(self.carplate,1):
                print("出库")
                sss+="车辆正在进行出库\n"
                #这里默认的是车库1，实际运用的话应当不同的车库的管理员改一下
                cash=inout.Leave(self.carplate,1)
                if cash=="Failed":
                    sss+="出现了错误"
                else:
                    usrid = inout.GetUserId(self.carplate)
                    import db_use
                    if db_use.hasvip(usrid):
                        sss += "尊敬的vip，进出停车场vip免费"
                    else:
                        sss+="您需要支付"+str(cash)+"元"
                        if states.autopay==False:
                            sss += "您未开启自动付款，请手动付款\n"
                    if states.autopay==True:
                        import db_use
                        import inout
                        usrid=inout.GetUserId(self.carplate)
                        if db_use.hasvip(usrid):
                            sss += "尊敬的vip，进出停车场vip免费"
                        else:
                            bal=db_use.getbalance(usrid)
                            if cash>bal:
                                sss += "余额不足，自动划款失败，请手动交给工作人员\n"
                            else:
                                db_use.addbalance(usrid,-cash)
                                sss += "已成功自动从余额划款\n"



            else:
                print("入库")
                sss += "车辆正在进行入库\n"
                #这里是默认的值
                inout.Enter(self.carplate,"default",1)
                sss+="已经成功入库"

            self.event_box.setPlainText(sss)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_loop.setText(_translate("MainWindow", "对照片进行检测"))
        self.btn_detect.setText(_translate("MainWindow", "进行拍照"))
        self.btn2.setText(_translate("MainWindow", "智能出入库"))
        self.checkBox_2.setText(_translate("MainWindow", "自动缴费"))
        self.checkBox_2.setStyleSheet("color: white; font-size: 22px;")
        self.checkBox_3.setText(_translate("MainWindow", "拍照后自动检测"))
        self.checkBox_3.setStyleSheet("color: white; font-size: 22px;")
        self.admin.setText(_translate("MainWindow", "进入管理员模式"))
        self.commandLinkButton.setText(_translate("MainWindow", "充值余额或升级vip"))
        self.cam_pic.setText(_translate("MainWindow", "捕获的图片"))
        self.chepai_pic.setText(_translate("MainWindow", "车牌"))
        self.cam_pic.setStyleSheet("""
        background-image: url('1.jpg');
                background-size: 100% ,100%;
                background-repeat: no-repeat;
                background-position: center;
        """)
        self.chepai_pic.setStyleSheet("""
               background-image: url('2.png');
                background-size: 100% ,100%;
                background-repeat: no-repeat;
                background-position: left;
               """)
        self.commandLinkButton.setStyleSheet('''
            QCommandLinkButton {
                background-color: #3498db;
                color: white;
                border-color: grey;
                border-style: solid;
                border-width: 1px;
                border-radius: 5px;
                padding: 10px;
                font-size: 22px;
            }
            QCommandLinkButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.btn_loop.setStyleSheet("""
            QCommandLinkButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-image: url('350.jpg');
                background-size: 100% ,100%;
                background-repeat: no-repeat;
                background-position: center;
            }
            
            QCommandLinkButton:hover {
                background-color: #2980b9;
            }
        """)
        self.admin.setStyleSheet('''
            QCommandLinkButton {
                background-color: #ADD8E6; /* 浅蓝色 */
                color: grey;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 24px;
            }
            QCommandLinkButton:hover {
                background-color: #87CEEB; /* 较亮的蓝色 */
            }
        ''')
        self.btn2.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                min-width: 60px;
                font-size: 18px;
                 font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.btn2.setFixedSize(150,60)
        self.btn_detect.setStyleSheet('''
            QCommandLinkButton {
                background-color:#bfffbf;
                color: #002a37;
                border: none;
                border-radius: 5px;
                padding: 10px;
                 font-size: 24px;
            }
            QCommandLinkButton:hover {
                background-color: #e7f3d5;
            }
        ''' )
        ui.event_box.appendPlainText("状态提示框：\n")




class state():
    def __init__(self):
        self.autopay=False
        self.autoscan=False



def autopay():
    states.autopay = not states.autopay;
    print("autopay" + str(states.autopay))


def autoscan():
    states.autoscan=not states.autoscan;
    # if states.autoscan:
    #     # ui.btn_loop.setEnabled(False)
    # else:
    #     ui.btn_loop.setEnabled(False)
    print("autoscan"+str(states.autoscan))


def once_step1():
    t0 = Thread(target=once_step0)
    t0.start()
    t0.join()
    print(states.autoscan)
    if states.autoscan==True:
        print("State2")
        ui.btn_loop.click()
        # t2 = Thread(target=once_step2)
        # t2.start()
        # t2.join()

def once_step0():
    print("step0")
    get_img.Getimg(ui.cam_pic.width(), ui.cam_pic.height())
    ui.cam_pic.setPixmap(QPixmap("cap.jpg"))

def once_step2():
    nums = getmask.Getmask("cap_raw.jpg")
    # print(nums)
    dist = "plate/CAR_" + str(nums) + ".jpg"
    if nums == -1:
        ui.cam_pic.setPixmap(QPixmap("CAR_RAW.jpg"))
        ui.chepai_pic.setPixmap(QPixmap("notfound.png"))
    else:
        from getmask import resize_image
        resize_image(dist,ui.chepai_pic.width()-90,ui.chepai_pic.height())
        resize_image("CAR_RAW.jpg", ui.cam_pic.width(), ui.cam_pic.height() )
        ui.cam_pic.setPixmap(QPixmap("CAR_RAW.jpg"))
        ui.chepai_pic.setPixmap(QPixmap(dist))
        print("preparing for ocr")
        PLATE = ocr.OCR_detail()
        print(PLATE)
        # 识别识别就拿识别到的最大的框中的内容作为识别结果
        if len(PLATE) == 0:
            PLATE = ocr.OCR_raw(dist)
            strs = ui.event_box.toPlainText() + "识别成功（但可能由于角度或清晰度原因有差错，请您确认）\n" + PLATE + '\n'
            ui.event_box.appendPlainText(strs)
            ui.carplate = PLATE
        else:
            print(PLATE)
            ui.carplate=PLATE
            strs = "识别成功:" + PLATE+"\n"
            ui.event_box.appendPlainText(strs)
def detect_once():
    t1 = Thread(target=once_step1)
    t1.start()



def func(name, sec):
    print('开始', name, '时间', ctime())
    sleep(sec)
    print('结束', name, '时间', ctime())

def detect_loop():
    print("detect_loop")
    once_step2()





app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
states=state()


MainWindow.show()

sys.exit(app.exec_())
