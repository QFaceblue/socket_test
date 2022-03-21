import os
import ssl
import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox

from crypto import Use_des, Use_des3, Use_aes
from guomi import Sm4


class Main(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/main.ui", self)
        self.IP = '192.168.8.101'
        # self.IP = '127.0.0.1'
        self.PORT = 50000
        self.buflen = 10240
        self.listensocket = None
        self.child = None
        self.cmdSocket = {}
        self.addrs = {}
        self.currentUser = None
        self.lineEdit_ip.setText(self.IP)
        self.lineEdit_port.setText(str(self.PORT))

        # 给按钮绑定函数
        self.btn_start.clicked.connect(
            lambda: self.create_t(self.start_listen))
        self.btn_nw.clicked.connect(self.new_window)
        self.safe_btn.clicked.connect(self.new_save)
        self.comboBox.currentIndexChanged.connect(self.selectionChange)

        # 设置按钮不可用
        self.btn_nw.setEnabled(False)
        # self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     '本程序',
                                     "是否要退出程序？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 新建线程处理，避免界面卡顿
    def create_t(self, func):
        th = Thread(target=func, args=())
        th.start()

    def start_listen(self):
        self.btn_start.setEnabled(False)
        self.IP = self.lineEdit_ip.text()
        self.PORT = self.lineEdit_port.text()
        if self.listensocket is None:
            listen_th = Thread(target=self.listen)
            listen_th.start()
        else:
            print("has started server ip:port={}:{} buflen={}"
                  .format(self.IP, self.PORT, self.buflen))

    def listen(self):
        print("server ip:port={}:{} buflen={}"
              .format(self.IP, self.PORT, self.buflen))
        # 实例化一个socket对象 用来监听视镜网端连接请求
        listensocket = socket(AF_INET, SOCK_STREAM)
        # socket绑定地址和端口
        listensocket.bind((self.IP, int(self.PORT)))
        listensocket.listen(8)
        self.listensocket = listensocket
        self.label_title.setText('等待视镜网端连接')
        while True:
            # 在循环中，一直接受新的连接请求
            datasocket, addr = self.listensocket.accept()
            addr = str(addr)
            print(f'一个视镜网端 {addr} 连接成功')

            recved = datasocket.recv(self.buflen)
            # 当对方关闭连接的时候，返回空字符串
            if not recved:
                print(f'视镜网端{addr} 关闭了连接')
                # break

            # 读取的字节数据是bytes类型，需要解码为字符串
            key = recved.decode("utf-8", "ignore")
            print(key)
            t, user = self.val(datasocket, key)
            if t:
                pass
            else:
                print("refuse")
                continue
            self.create_socket(datasocket, addr, user)
            # recved = datasocket.recv(self.buflen)
            # info = recved.decode("utf-8", "ignore")
            # print(info)
            # if info == "cmd":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.cmd, args=(datasocket, addr, user))
            #     th.start()
            #     print(f'视镜网端用户{user}:{addr} 连接成功!')
            # elif info == "send_file":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.sendfile, args=(datasocket, addr))
            #     th.start()
            # elif info == "update":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.update, args=(datasocket, addr))
            #     th.start()
            # elif info == "short":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.short, args=(datasocket, addr))
            #     th.start()
            # elif info == "short_sm4":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.short_sm4, args=(datasocket, addr))
            #     th.start()
            # elif info == "short_des":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.short_des, args=(datasocket, addr))
            #     th.start()
            # elif info == "short_des3":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.short_des3, args=(datasocket, addr))
            #     th.start()
            # elif info == "short_aes":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.short_aes, args=(datasocket, addr))
            #     th.start()
            # elif info == "record":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.getRecord, args=(datasocket, addr))
            #     th.start()
            # else:
            #     datasocket.send("no".encode())
            #     print("一个连接被拒绝！")

        self.listensocket.close()

    def create_socket(self, datasocket, addr, user):
        recved = datasocket.recv(self.buflen)
        info = recved.decode("utf-8", "ignore")
        print(info)
        if info == "cmd":
            datasocket.send("yes".encode())
            th = Thread(target=self.cmd, args=(datasocket, addr, user))
            th.start()
            print(f'视镜网端用户{user}:{addr} 连接成功!')
        elif info == "send_file":
            datasocket.send("yes".encode())
            th = Thread(target=self.sendfile, args=(datasocket, addr))
            th.start()
        elif info == "update":
            datasocket.send("yes".encode())
            th = Thread(target=self.update, args=(datasocket, addr))
            th.start()
        elif info == "short":
            datasocket.send("yes".encode())
            th = Thread(target=self.short, args=(datasocket, addr))
            th.start()
        elif info == "short_sm4":
            datasocket.send("yes".encode())
            th = Thread(target=self.short_sm4, args=(datasocket, addr))
            th.start()
        elif info == "short_des":
            datasocket.send("yes".encode())
            th = Thread(target=self.short_des, args=(datasocket, addr))
            th.start()
        elif info == "short_des3":
            datasocket.send("yes".encode())
            th = Thread(target=self.short_des3, args=(datasocket, addr))
            th.start()
        elif info == "short_aes":
            datasocket.send("yes".encode())
            th = Thread(target=self.short_aes, args=(datasocket, addr))
            th.start()
        elif info == "record":
            datasocket.send("yes".encode())
            th = Thread(target=self.getRecord, args=(datasocket, addr))
            th.start()
        else:
            datasocket.send("no".encode())
            print("一个连接被拒绝！")

    def val(self, socket, key):
        key = key.split(" ")
        if len(key) < 2:
            socket.send("refuse_1".encode())
            return False, None
        user = key[0]
        password = key[1]
        users = {}
        for i in range(1, 90):
            name = "user" + str(i)
            pwd = "password" + str(i)
            users[name] = pwd
        print(users)
        if users.get(user, None) is not None:
            if users[user] == password:
                socket.send("pass".encode())
                return True, user
            else:
                socket.send("refuse_2".encode())
                return False, None
        else:
            socket.send("refuse_3".encode())
            return False, None

    def cmd(self, datasocket, addr, user):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"ready":
            self.label_title.setText(f'用户：{user} {addr} 连接成功')
            self.cmdSocket[user] = datasocket
            self.addrs[user] = addr
            self.comboBox.addItem(user)
            self.currentUser = user
            self.btn_nw.setEnabled(True)

    def new_window(self):
        print("add")
        self.child = Childui(self.currentUser,
                             self.cmdSocket[self.currentUser],
                             self.addrs[self.currentUser])
        # self.child = Childui()
        print("before")
        print(self.child.my_signal[str])
        self.child.my_signal[str].connect(self.child_exit)
        print("after")
        self.child.show()
        self.btn_nw.setEnabled(False)

    def new_save(self):

        self.socketui = Socketui()
        self.socketui.ssl_signal[str].connect(self.socket_exit)
        self.socketui.show()
        # socket_ui = Socketui()
        # socket_ui.ssl_signal[str].connect(self.socket_exit)
        # socket_ui.show()
        self.safe_btn.setEnabled(False)

    def child_exit(self, user):
        print(user + "子窗口关闭")
        self.btn_nw.setEnabled(True)

    def socket_exit(self, s):
        print("接受安全通道关闭信号" + s)
        self.safe_btn.setEnabled(True)

    def selectionChange(self):
        print(self.comboBox.currentIndex(), self.comboBox.currentText())
        self.currentUser = self.comboBox.currentText()

    def test(self):
        print("test")

    def short(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"start":

            self.shortSocket = datasocket
            print("short connect!")
            text = self.child.lineEdit_short.text()
            if text != "":
                start = time.time()
                times = int(self.child.lineEdit_short_time.text())
                pre_progress = 0
                text = text.encode()
                # progressBar_short = self.progressBar_short
                for i in range(times):
                    # print(recved.decode()+"1")
                    datasocket.send(text)
                    # print(recved.decode()+"2")
                    recved = datasocket.recv(buflen)
                    # print(recved.decode()+"3")
                    cur_progress = int((i + 1) / times * 100)
                    print(cur_progress)
                    if cur_progress > pre_progress:
                        print(cur_progress)
                        # progressBar_short.setValue(cur_progress)
                        self.child.label_short_result.setText(
                            "发送中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                    # print(recved.decode()+"4")
                datasocket.send("end".encode())
                self.child.label_short_result.setText(
                    "发送{}次消息(视镜网端返回值为：{})，""总共花费时间为：{:6f}".format(
                        times, recved.decode(), time.time() - start))
            else:
                self.child.label_short_result.setText("输入为空值！")

        self.child.btn_short.setEnabled(True)

    def short_sm4(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"start":

            self.shortSocket = datasocket
            print("short connect!")
            text = self.child.lineEdit_short_sm4.text()
            if text != "":
                start = time.time()
                times = int(self.child.lineEdit_short_time_sm4.text())
                pre_progress = 0
                # text = text.encode()
                # progressBar_short = self.progressBar_short
                sm4 = Sm4()
                text_e = sm4.encrypt(text)
                self.child.label_sm4.setText("密文：{}%".format(text_e))
                e_s = time.time()
                for i in range(times):
                    text_e = sm4.encrypt(text)
                total_e = time.time() - e_s
                for i in range(times):
                    # print(recved.decode()+"1")
                    datasocket.send(text_e.encode())
                    # print(recved.decode()+"2")
                    recved = datasocket.recv(buflen)
                    # print(recved.decode()+"3")
                    cur_progress = int((i + 1) / times * 100)
                    print(cur_progress)
                    if cur_progress > pre_progress:
                        print(cur_progress)
                        # progressBar_short.setValue(cur_progress)
                        self.child.label_short_result_sm4.setText(
                            "发送中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                    # print(recved.decode()+"4")
                datasocket.send("end".encode())
                self.child.label_short_result_sm4.setText(
                    "发送{}次消息(视镜网端返回值为：{})，总加密时间为：{:6f}，总共花费时间为：{:6f}".format(
                        times, recved.decode(), total_e, time.time() - start))
            else:
                self.child.label_short_result_sm4.setText("输入为空值！")

        self.child.btn_short_sm4.setEnabled(True)

    def short_des(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"start":

            self.shortSocket = datasocket
            print("short connect!")
            text = self.child.lineEdit_short_des.text()
            if text != "":
                start = time.time()
                times = int(self.child.lineEdit_short_time_des.text())
                pre_progress = 0
                # text = text.encode()
                # progressBar_short = self.progressBar_short
                des_test = Use_des(b"12345678")
                text_e = des_test.encrypt(text)
                self.child.label_des.setText("密文：{}%".format(text_e))
                e_s = time.time()
                for i in range(times):
                    text_e = des_test.encrypt(text)
                total_e = time.time() - e_s
                for i in range(times):
                    # print(recved.decode()+"1")
                    datasocket.send(text_e)
                    # print(recved.decode()+"2")
                    recved = datasocket.recv(buflen)
                    # print(recved.decode()+"3")
                    cur_progress = int((i + 1) / times * 100)
                    print(cur_progress)
                    if cur_progress > pre_progress:
                        print(cur_progress)
                        # progressBar_short.setValue(cur_progress)
                        self.child.label_short_result_des.setText(
                            "发送中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                    # print(recved.decode()+"4")
                datasocket.send("end".encode())
                self.child.label_short_result_des.setText(
                    "发送{}次消息(视镜网端返回值为：{})，总加密时间为：{:6f}，总共花费时间为：{:6f}".format(
                        times, recved.decode(), total_e, time.time() - start))
            else:
                self.child.label_short_result_des.setText("输入为空值！")

        self.child.btn_short_des.setEnabled(True)

    def short_des3(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"start":

            self.shortSocket = datasocket
            print("short connect!")
            text = self.child.lineEdit_short_des3.text()
            if text != "":
                start = time.time()
                times = int(self.child.lineEdit_short_time_des3.text())
                pre_progress = 0
                # text = text.encode()
                # progressBar_short = self.progressBar_short
                des3_test = Use_des3(b"123456789qazxswe")
                text_e = des3_test.encrypt(text)
                self.child.label_des3.setText("密文：{}%".format(text_e))
                e_s = time.time()
                for i in range(times):
                    text_e = des3_test.encrypt(text)
                total_e = time.time() - e_s
                for i in range(times):
                    # print(recved.decode()+"1")
                    # text_e = des3_test.encrypt(text)
                    datasocket.send(text_e)
                    # print(recved.decode()+"2")
                    recved = datasocket.recv(buflen)
                    # print(recved.decode()+"3")
                    cur_progress = int((i + 1) / times * 100)
                    print(cur_progress)
                    if cur_progress > pre_progress:
                        print(cur_progress)
                        # progressBar_short.setValue(cur_progress)
                        self.child.label_short_result_des3.setText(
                            "发送中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                    # print(recved.decode()+"4")
                datasocket.send("end".encode())
                self.child.label_short_result_des3.setText(
                    "发送{}次消息(视镜网端返回值为：{})，总加密时间为：{:6f}，总共花费时间为：{:6f}".format(
                        times, recved.decode(), total_e, time.time() - start))
            else:
                self.child.label_short_result_des3.setText("输入为空值！")

        self.child.btn_short_des3.setEnabled(True)

    def short_aes(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"start":

            self.shortSocket = datasocket
            print("short connect!")
            text = self.child.lineEdit_short_aes.text()
            if text != "":
                start = time.time()
                times = int(self.child.lineEdit_short_time_aes.text())
                pre_progress = 0
                # text = text.encode()
                # progressBar_short = self.progressBar_short
                aes_test = Use_aes("assssssssdfasasasasa")
                text_e = aes_test.encrypt(text)
                self.child.label_aes.setText("密文：{}%".format(text_e.encode()))
                e_s = time.time()
                for i in range(times):
                    text_e = aes_test.encrypt(text)
                total_e = time.time() - e_s
                for i in range(times):
                    # print(recved.decode()+"1")
                    # text_e = aes_test.encrypt(text)
                    datasocket.send(text_e.encode())
                    # print(recved.decode()+"2")
                    recved = datasocket.recv(buflen)
                    # print(recved.decode()+"3")
                    cur_progress = int((i + 1) / times * 100)
                    print(cur_progress)
                    if cur_progress > pre_progress:
                        print(cur_progress)
                        # progressBar_short.setValue(cur_progress)
                        self.child.label_short_result_aes.setText(
                            "发送中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                    # print(recved.decode()+"4")
                datasocket.send("end".encode())
                self.child.label_short_result_aes.setText(
                    "发送{}次消息(视镜网端返回值为：{})，总加密时间为：{:6f}，总共花费时间为：{:6f}".format(
                        times, recved.decode(), total_e, time.time() - start))
            else:
                self.child.label_short_result_aes.setText("输入为空值！")

        self.child.btn_short_aes.setEnabled(True)

    def gps_save(self, datasocket, addr):
        buflen = self.buflen
        log_path = "./logs"
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        file_name = "gps_{}.txt".format(
            time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
        file_path = os.path.join(log_path, file_name)
        datasocket.settimeout(60)
        print("save gps")
        f = open(file_path, "w")
        while True:
            try:
                recved = datasocket.recv(buflen)
                if recved == b"exit":
                    print(recved)
                    f.flush()
                    f.close()
                    break
            except Exception as e:
                print(e)
                f.flush()
                f.close()
                datasocket.close()
                break
            # 当对方关闭连接的时候，返回空字符串
            if not recved:
                print(f'视镜网端{addr} 关闭了连接')
                break

            # 读取的字节数据是bytes类型，需要解码为字符串
            info = recved.decode("utf-8", "ignore")
            f.write(info + "\n")
            f.flush()
            send = datasocket.send(f'服务端接收到了信息 {info}'.encode())
            print(send)
        datasocket.close()

    # 客户获取文件
    def getfile(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        file_name = recved.decode("utf-8", "ignore")
        path = os.path.join("./weights", file_name)
        if os.path.exists(path) and os.path.isfile(path):
            print(path)
            datasocket.send("start".encode())

            with open(path, "rb") as f:
                while True:
                    data = f.read(buflen)
                    if len(data) == 0:
                        break
                    datasocket.send(data)
                print("doned")
            datasocket.send("doned".encode())
        else:
            datasocket.send("not existed".encode())
        datasocket.close()
        print("close")

    # 客户获取文件
    def sendfile(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        start = time.time()
        if recved == b"ok":
            uploadfile = self.child.uploadfile
            print(uploadfile)
            file_name = os.path.basename(uploadfile)
            datasocket.send(file_name.encode())
            recved = datasocket.recv(buflen)

            datasocket.send("start".encode())
            size = int(os.path.getsize(uploadfile) / buflen) + 1
            count = 0
            pre_progress = 0
            # progressBar_upload = self.progressBar_upload
            with open(uploadfile, "rb") as f:
                # for data in f:
                #     datasocket.send(data)
                #     # print(data)
                while True:
                    data = f.read(buflen)
                    if len(data) == 0:
                        break
                    datasocket.send(data)
                    count += 1
                    cur_progress = int(count / size * 100)
                    if cur_progress > pre_progress:
                        print(count, size)
                        # progressBar_upload.setValue(cur_progress)
                        self.child.label_file_result.setText(
                            "上传中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                print("doned")
            datasocket.send("doned".encode())
        else:
            datasocket.send("not existed".encode())

        datasocket.close()
        self.child.label_file_result.setText(
            "成功上传文件：{}, 共使用{:.6f}秒".format(
                os.path.basename(self.child.uploadfile), time.time() - start))
        print("close")

    # 获取用户违规记录
    def getRecord(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        if recved == b"ready":
            # 获取当前最新记录
            base_path = "./record_s2"
            if not os.path.isdir(base_path):
                os.makedirs(base_path)
            dirs = os.listdir(base_path)
            if len(dirs) > 0:
                dirs.sort()
                new_dir = dirs[-1]
                dir_path = os.path.join(base_path, new_dir)
                imgs = os.listdir(dir_path)
                imgs.sort()
                if len(imgs) < 1:
                    new_img = new_dir
                else:
                    new_img = imgs[-1]
            else:
                new_img = "all"
            datasocket.send(new_img.encode())
            self.get_imgs(datasocket, base_path)
        datasocket.close()
        print("close")

    def get_imgs(self, datasocket, base_path):
        buflen = self.buflen
        count = 0
        start = time.time()
        while True:

            recved = datasocket.recv(buflen)
            if recved == b"finished" or recved == b"":
                if count == 0:
                    self.child.label_record_result.setText(
                        "没有新的违规记录，共使用{:.6f}秒".format(
                            time.time() - start))
                else:
                    self.child.label_record_result.setText(
                        "更新{}张违规记录，共使用{:.6f}秒".format(
                            count, time.time() - start))
                break
            if recved == b"dir":
                datasocket.send("yes".encode())
                recved = datasocket.recv(buflen)
                recved = recved.decode("utf-8", "ignore")
                dir_path = os.path.join(base_path, recved)
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path)
                datasocket.send("start_dir".encode())
                while True:
                    recved = datasocket.recv(buflen)
                    if recved == b"dir_finished":
                        datasocket.send("dir_finished".encode())
                        break
                    recved = recved.decode("utf-8", "ignore")
                    datasocket.send("start_img".encode())
                    img_path = os.path.join(dir_path, recved)
                    with open(img_path, "wb") as f:
                        while True:
                            recved = datasocket.recv(buflen)
                            if recved.endswith(b"doned") or recved == b'':
                                print("got {}".format(img_path))
                                datasocket.send("doned".encode())
                                break
                            f.write(recved)
                    count += 1

    # 客户获取最新权重
    def update(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        cname = recved.decode("utf-8", "ignore")
        versions = os.listdir("./versions")
        versions.sort(key=lambda x: x.split("_")[1])
        filename = versions[-1]
        print(filename)
        start = time.time()
        if cname == filename:
            datasocket.send("newest".encode())
            self.child.label_weight_result.setText(
                "已经是最新版本! 共使用:{:6f}秒".format(
                    time.time() - start))
        else:
            path = os.path.join("./versions", filename)
            print(path)
            if os.path.exists(path) and os.path.isfile(path):
                datasocket.send(filename.encode())

                with open(path, "rb") as f:
                    while True:
                        data = f.read(buflen)
                        if len(data) == 0:
                            break
                        datasocket.send(data)
                    print("doned")
                datasocket.send("doned".encode())
            self.child.label_weight_result.setText(
                "更新：{} 共使用:{:6f}秒".format(
                    filename, time.time() - start))
        datasocket.close()
        print("close")


class Childui(QWidget):

    def __init__(self, user=None, socket=None, addr=None):
        super().__init__()
        uic.loadUi("./ui/child.ui", self)
        self.uploadfile = ""
        self.IP = '192.168.8.101'
        # self.IP = '127.0.0.1'
        self.PORT = 50000
        self.buflen = 10240
        self.user = user
        self.cmdSocket = socket
        self.addr = addr
        self.label_title.setText("用户：{} 地址:{}".format(self.user, self.addr))
        self.lineEdit_short.setText("测试！")
        self.lineEdit_short_time.setText("100")
        self.lineEdit_short_sm4.setText("测试SM4加密！")
        self.lineEdit_short_time_sm4.setText("100")
        self.lineEdit_short_des.setText("测试DES加密！")
        self.lineEdit_short_time_des.setText("100")
        self.lineEdit_short_des3.setText("测试DES3加密！")
        self.lineEdit_short_time_des3.setText("100")
        self.lineEdit_short_aes.setText("测试AES加密！")
        self.lineEdit_short_time_aes.setText("100")
        # 绑定函数
        self.btn_record.clicked.connect(
            lambda: self.create_t(self.get_record))
        self.btn_weight.clicked.connect(
            lambda: self.create_t(self.update_weight))
        self.btn_short.clicked.connect(
            lambda: self.create_t(self.send_short))
        self.btn_short_sm4.clicked.connect(
            lambda: self.create_t(self.send_short_sm4))
        self.btn_short_des.clicked.connect(
            lambda: self.create_t(self.send_short_des))
        self.btn_short_des3.clicked.connect(
            lambda: self.create_t(self.send_short_des3))
        self.btn_short_aes.clicked.connect(
            lambda: self.create_t(self.send_short_aes))
        self.btn_choose.clicked.connect(
            lambda: self.create_t(self.choose_file()))
        self.btn_upload.clicked.connect(
            lambda: self.create_t(self.upload_file))
        self.btn_upload.setEnabled(False)

        # 让多窗口之间传递信号 刷新主窗口信息

    my_signal = QtCore.pyqtSignal(str)

    def closeEvent(self, event):
        print(self.user + "子窗口关闭")
        self.my_signal.emit(self.user)

    # 新建线程处理，避免界面卡顿
    def create_t(self, func):
        th = Thread(target=func, args=())
        th.start()

    def get_record(self):
        self.label_record_result.setText("downloading......")
        self.cmdSocket.send("upload_record".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())

    def update_weight(self):
        self.label_weight_result.setText("updating......")
        self.cmdSocket.send("update_weight".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())

    def send_short(self):
        self.label_short_result.setText("发送中...... 0%")
        self.cmdSocket.send("short".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_short.setEnabled(False)

    def send_short_sm4(self):
        self.label_short_result_sm4.setText("发送中...... 0%")
        self.cmdSocket.send("short_sm4".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_short_sm4.setEnabled(False)

    def send_short_des(self):
        self.label_short_result_des.setText("发送中...... 0%")
        self.cmdSocket.send("short_des".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_short_des.setEnabled(False)

    def send_short_des3(self):
        self.label_short_result_des3.setText("发送中...... 0%")
        self.cmdSocket.send("short_des3".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_short_des3.setEnabled(False)

    def send_short_aes(self):
        self.label_short_result_aes.setText("发送中...... 0%")
        self.cmdSocket.send("short_aes".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_short_aes.setEnabled(False)

    def choose_file(self):
        # print("choose source")
        file, _ = QFileDialog.getOpenFileName(self, '选择上传文件', './file')
        print("upload_file:", file)
        if file != "":
            self.lineEdit_file.setText(file)
            self.uploadfile = file
            # 设置按钮可用
            self.btn_upload.setEnabled(True)
            # 设置按钮不可用
            self.btn_choose.setEnabled(False)
            # # 设置进度条
            # self.progressBar_upload.setValue(0)

    def upload_file(self):
        self.label_file_result.setText("上传中...... 0%")
        self.cmdSocket.send("send_file".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_upload.setEnabled(False)
        self.btn_choose.setEnabled(True)

    def val(self, socket, key):
        key = key.split(" ")
        if len(key) < 2:
            socket.send("refuse".encode())
            return False, None
        user = key[0]
        password = key[1]
        users = {}
        users["user101"] = "password101"
        users["user102"] = "password102"
        users["user103"] = "password103"
        if users.get(user, None) is not None:
            if users[user] == password:
                socket.send("pass".encode())
                return True, user
            else:
                socket.send("refuse".encode())
                return False, None
        else:
            socket.send("refuse".encode())
            return False, None


class Socketui(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/socket_ssl.ui", self)

        self.uploadfile = ""
        self.IP = '192.168.8.101'
        # self.IP = '127.0.0.1'
        self.PORT = 50001
        self.buflen = 10240
        self.listensocket = None
        self.stop = True
        self.cmdSocket = None
        self.lineEdit_ip.setText(self.IP)
        self.lineEdit_port.setText(str(self.PORT))
        self.lineEdit_short.setText("测试！")
        self.lineEdit_short_time.setText("100")
        # 绑定函数
        self.btn_start.clicked.connect(
            lambda: self.create_t(self.start_listen))
        self.btn_record.clicked.connect(
            lambda: self.create_t(self.get_record))
        self.btn_weight.clicked.connect(
            lambda: self.create_t(self.update_weight))
        self.btn_short.clicked.connect(
            lambda: self.create_t(self.send_short))
        self.btn_choose.clicked.connect(
            lambda: self.create_t(self.choose_file()))
        self.btn_upload.clicked.connect(
            lambda: self.create_t(self.upload_file))
        # 设置按钮不可用
        self.btn_record.setEnabled(False)
        self.btn_weight.setEnabled(False)
        self.btn_short.setEnabled(False)
        self.btn_choose.setEnabled(False)
        self.btn_upload.setEnabled(False)

    ssl_signal = QtCore.pyqtSignal(str)

    def closeEvent(self, event):
        print("安全通道关闭")
        self.ssl_signal.emit("ssl")
        self.stop = True
        if self.listensocket is not None:
            self.listensocket.close()

    # 新建线程处理，避免界面卡顿
    def create_t(self, func):
        th = Thread(target=func, args=())
        th.start()

    def get_record(self):
        self.label_record_result.setText("downloading......")
        self.cmdSocket.send("upload_record".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())

    def update_weight(self):
        self.label_weight_result.setText("updating......")
        self.cmdSocket.send("update_weight".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())

    def send_short(self):
        self.label_short_result.setText("发送中...... 0%")
        self.cmdSocket.send("short".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_short.setEnabled(False)

    def short(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"start":

            self.shortSocket = datasocket
            print("short connect!")
            text = self.lineEdit_short.text()
            if text != "":
                start = time.time()
                times = int(self.lineEdit_short_time.text())
                pre_progress = 0
                text = text.encode()
                # progressBar_short = self.progressBar_short
                for i in range(times):
                    # print(recved.decode()+"1")
                    datasocket.send(text)
                    # print(recved.decode()+"2")
                    recved = datasocket.recv(buflen)
                    # print(recved.decode()+"3")
                    cur_progress = int((i + 1) / times * 100)
                    print(cur_progress)
                    if cur_progress > pre_progress:
                        print(cur_progress)
                        # progressBar_short.setValue(cur_progress)
                        self.label_short_result.setText("发送中...... {}%"
                                                        .format(cur_progress))
                        pre_progress = cur_progress
                    # print(recved.decode()+"4")
                datasocket.send("end".encode())
                self.label_short_result.setText(
                    "发送{}次消息(视镜网端返回值为：{})，总共花费时间为：{:6f}".format(
                        times, recved.decode(), time.time() - start))
            else:
                self.label_short_result.setText("输入为空值！")

        self.btn_short.setEnabled(True)

    def choose_file(self):
        # print("choose source")
        file, _ = QFileDialog.getOpenFileName(self, '选择上传文件', './file')
        print("upload_file:", file)
        if file != "":
            self.lineEdit_file.setText(file)
            self.uploadfile = file
            # 设置按钮可用
            self.btn_upload.setEnabled(True)
            # 设置按钮不可用
            self.btn_choose.setEnabled(False)
            # # 设置进度条
            # self.progressBar_upload.setValue(0)

    def upload_file(self):
        self.label_file_result.setText("上传中...... 0%")
        self.cmdSocket.send("send_file".encode())
        recved = self.cmdSocket.recv(self.buflen)
        print(recved.decode())
        self.btn_upload.setEnabled(False)
        self.btn_choose.setEnabled(True)

    def start_listen(self):
        self.btn_start.setEnabled(False)
        self.IP = self.lineEdit_ip.text()
        self.PORT = self.lineEdit_port.text()
        if self.listensocket is None:
            listen_th = Thread(target=self.listen)
            listen_th.start()
        else:
            print("has started server ip:port={}:{} buflen={}"
                  .format(self.IP, self.PORT, self.buflen))

    def listen(self):
        print("server ip:port={}:{} buflen={}"
              .format(self.IP, self.PORT, self.buflen))
        # 实例化一个socket对象 用来监听视镜网端连接请求
        listensocket = socket(AF_INET, SOCK_STREAM)
        # socket绑定地址和端口
        listensocket.bind((self.IP, int(self.PORT)))
        listensocket.listen(8)
        # 生成SSL上下文
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # 加载服务器所用证书和私钥
        context.load_cert_chain('CA2/server.crt', 'CA2/server.key')
        listensocket = context.wrap_socket(listensocket, server_side=True)
        self.listensocket = listensocket
        self.stop = False
        self.label_title.setText('等待视镜网端连接')
        while True:
            # 在循环中，一直接受新的连接请求
            if self.stop:
                break
            try:
                datasocket, addr = self.listensocket.accept()
            except Exception as e:
                print(e)
                return
            # datasocket, addr = self.listensocket.accept()
            # Establish connection with client.
            addr = str(addr)
            print(f'一个视镜网端 {addr} 连接成功')

            recved = datasocket.recv(self.buflen)
            # 当对方关闭连接的时候，返回空字符串
            if not recved:
                print(f'视镜网端{addr} 关闭了连接')
                # break

            # 读取的字节数据是bytes类型，需要解码为字符串
            key = recved.decode("utf-8", "ignore")
            print(key)
            if self.val(datasocket, key):
                pass
            else:
                print("refuse")
                continue
            self.create_socket(datasocket, addr)
            # recved = datasocket.recv(self.buflen)
            # info = recved.decode("utf-8", "ignore")
            # print(info)
            # if info == "gps":
            #     datasocket.send("yes".encode())
            #     # 创建新线程处理和这个视镜网端的消息收发
            #     th = Thread(target=self.gps_save, args=(datasocket, addr))
            #     th.start()
            # elif info == "send_file":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.sendfile, args=(datasocket, addr))
            #     th.start()
            # elif info == "update":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.update, args=(datasocket, addr))
            #     th.start()
            # elif info == "short":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.short, args=(datasocket, addr))
            #     th.start()
            # elif info == "cmd":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.cmd, args=(datasocket, addr))
            #     th.start()
            # elif info == "record":
            #     datasocket.send("yes".encode())
            #     th = Thread(target=self.getRecord, args=(datasocket, addr))
            #     th.start()
        self.listensocket.close()

    def create_socket(self, datasocket, addr):
        recved = datasocket.recv(self.buflen)
        info = recved.decode("utf-8", "ignore")
        print(info)
        if info == "gps":
            datasocket.send("yes".encode())
            # 创建新线程处理和这个视镜网端的消息收发
            th = Thread(target=self.gps_save, args=(datasocket, addr))
            th.start()
        elif info == "send_file":
            datasocket.send("yes".encode())
            th = Thread(target=self.sendfile, args=(datasocket, addr))
            th.start()
        elif info == "update":
            datasocket.send("yes".encode())
            th = Thread(target=self.update, args=(datasocket, addr))
            th.start()
        elif info == "short":
            datasocket.send("yes".encode())
            th = Thread(target=self.short, args=(datasocket, addr))
            th.start()
        elif info == "cmd":
            datasocket.send("yes".encode())
            th = Thread(target=self.cmd, args=(datasocket, addr))
            th.start()
        elif info == "record":
            datasocket.send("yes".encode())
            th = Thread(target=self.getRecord, args=(datasocket, addr))
            th.start()

    def gps_save(self, datasocket, addr):
        buflen = self.buflen
        log_path = "./logs"
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        file_name = "gps_{}.txt".format(
            time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
        file_path = os.path.join(log_path, file_name)
        datasocket.settimeout(60)
        print("save gps")
        f = open(file_path, "w")
        while True:
            try:
                recved = datasocket.recv(buflen)
                if recved == b"exit":
                    print(recved)
                    f.flush()
                    f.close()
                    break
            except Exception as e:
                print(e)
                f.flush()
                f.close()
                datasocket.close()
                break
            # 当对方关闭连接的时候，返回空字符串
            if not recved:
                print(f'视镜网端{addr} 关闭了连接')
                break

            # 读取的字节数据是bytes类型，需要解码为字符串
            info = recved.decode("utf-8", "ignore")
            f.write(info + "\n")
            # f.write(info)
            f.flush()
            # print(f'收到{addr}信息： {info}')
            # print(time.strftime("%H-%M-%S", time.localtime()))
            send = datasocket.send(f'服务端接收到了信息 {info}'.encode())
            print(send)
        datasocket.close()

    # 客户获取文件
    def getfile(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        file_name = recved.decode("utf-8", "ignore")
        path = os.path.join("./weights", file_name)
        if os.path.exists(path) and os.path.isfile(path):
            print(path)
            datasocket.send("start".encode())

            with open(path, "rb") as f:
                # for data in f:
                #     datasocket.send(data)
                #     # print(data)
                while True:
                    data = f.read(buflen)
                    if len(data) == 0:
                        break
                    datasocket.send(data)
                print("doned")
            datasocket.send("doned".encode())
        else:
            datasocket.send("not existed".encode())
        datasocket.close()
        print("close")

    # 客户获取文件
    def sendfile(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        start = time.time()
        if recved == b"ok":
            uploadfile = self.uploadfile
            print(uploadfile)
            file_name = os.path.basename(uploadfile)
            datasocket.send(file_name.encode())
            recved = datasocket.recv(buflen)

            datasocket.send("start".encode())
            size = int(os.path.getsize(uploadfile) / buflen) + 1
            count = 0
            pre_progress = 0
            # progressBar_upload = self.progressBar_upload
            with open(uploadfile, "rb") as f:
                while True:
                    data = f.read(buflen)
                    if len(data) == 0:
                        break
                    datasocket.send(data)
                    count += 1
                    cur_progress = int(count / size * 100)
                    if cur_progress > pre_progress:
                        print(count, size)
                        # progressBar_upload.setValue(cur_progress)
                        self.label_file_result.setText(
                            "上传中...... {}%".format(cur_progress))
                        pre_progress = cur_progress
                print("doned")
            datasocket.send("doned".encode())
        else:
            datasocket.send("not existed".encode())

        datasocket.close()
        self.label_file_result.setText(
            "成功上传文件：{}, 共使用{:.6f}秒".format(
                os.path.basename(self.uploadfile), time.time() - start))
        print("close")

    # 获取用户违规记录
    def getRecord(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        if recved == b"ready":
            # 获取当前最新记录
            base_path = "./record_s2_ssl"
            if not os.path.isdir(base_path):
                os.makedirs(base_path)
            dirs = os.listdir(base_path)
            if len(dirs) > 0:
                dirs.sort()
                new_dir = dirs[-1]
                dir_path = os.path.join(base_path, new_dir)
                imgs = os.listdir(dir_path)
                imgs.sort()
                if len(imgs) < 1:
                    new_img = new_dir
                else:
                    new_img = imgs[-1]
            else:
                new_img = "all"
            datasocket.send(new_img.encode())
            self.get_imgs(datasocket, base_path)

        datasocket.close()
        print("close")

    def get_imgs(self, datasocket, base_path):
        buflen = self.buflen
        count = 0
        start = time.time()
        while True:

            recved = datasocket.recv(buflen)
            if recved == b"finished" or recved == b"":
                if count == 0:
                    self.label_record_result.setText(
                        "没有新的违规记录，共使用{:.6f}秒".format(
                            time.time() - start))
                else:
                    self.label_record_result.setText(
                        "更新{}张违规记录，共使用{:.6f}秒".format(
                            count, time.time() - start))
                break
            if recved == b"dir":
                datasocket.send("yes".encode())
                recved = datasocket.recv(buflen)
                recved = recved.decode("utf-8", "ignore")
                dir_path = os.path.join(base_path, recved)
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path)
                datasocket.send("start_dir".encode())
                while True:
                    recved = datasocket.recv(buflen)
                    if recved == b"dir_finished":
                        datasocket.send("dir_finished".encode())
                        break
                    recved = recved.decode("utf-8", "ignore")
                    datasocket.send("start_img".encode())
                    img_path = os.path.join(dir_path, recved)
                    with open(img_path, "wb") as f:
                        while True:
                            recved = datasocket.recv(buflen)
                            if recved.endswith(b"doned") or recved == b'':
                                print("got {}".format(img_path))
                                datasocket.send("doned".encode())
                                break
                            f.write(recved)
                    count += 1

    # 客户获取最新权重
    def update(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if not recved:
            print(f'视镜网端{addr} 关闭了连接')
            return
        cname = recved.decode("utf-8", "ignore")
        versions = os.listdir("./versions")
        versions.sort(key=lambda x: x.split("_")[1])
        filename = versions[-1]
        print(filename)
        start = time.time()
        if cname == filename:
            datasocket.send("newest".encode())
            self.label_weight_result.setText("已经是最新版本! 共使用:{:6f}秒"
                                             .format(time.time() - start))
        else:
            path = os.path.join("./versions", filename)
            print(path)
            if os.path.exists(path) and os.path.isfile(path):
                datasocket.send(filename.encode())

                with open(path, "rb") as f:
                    while True:
                        data = f.read(buflen)
                        if len(data) == 0:
                            break
                        datasocket.send(data)
                    print("doned")
                datasocket.send("doned".encode())
            self.label_weight_result.setText(
                "更新：{} 共使用:{:6f}秒".format(
                    filename, time.time() - start))
        datasocket.close()
        print("close")

    def cmd(self, datasocket, addr):
        buflen = self.buflen
        recved = datasocket.recv(buflen)
        # 当对方关闭连接的时候，返回空字符串
        if recved == b"ready":
            self.label_title.setText(f'一个视镜网端 {addr} 连接成功')
            self.cmdSocket = datasocket
            self.btn_record.setEnabled(True)
            self.btn_weight.setEnabled(True)
            self.btn_short.setEnabled(True)
            self.btn_choose.setEnabled(True)
            # self.btn_upload.setEnabled(True)
            print("test")

    def val(self, socket, key):
        key = key.split(" ")
        if len(key) < 2:
            socket.send("refuse_1".encode())
            return False, None
        user = key[0]
        password = key[1]
        users = {}
        for i in range(1, 110):
            name = "user" + str(i)
            pwd = "password" + str(i)
            users[name] = pwd
        print(users)
        if users.get(user, None) is not None:
            if users[user] == password:
                socket.send("pass".encode())
                return True, user
            else:
                socket.send("refuse_2".encode())
                return False, None
        else:
            socket.send("refuse_3".encode())
            return False, None


if __name__ == '__main__':
    app = QApplication([])
    # 设置程序图标
    app.setWindowIcon(QIcon('./imgs/uestc.jpg'))
    # child_ui = Childui()
    # child_ui.ui.show()
    # socket_ui = Socketui()
    # socket_ui.show()
    main_ui = Main()
    main_ui.show()
    app.exec_()
    # sys.exit(app.exec_())
