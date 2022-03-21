#  === TCP 客户端程序 client.py ===
import os
import random
import ssl
import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

ip = '192.168.8.101'
# ip = '127.0.0.1'
server_port = 50001
buflen = 10240
# use_ssl = False
use_ssl = True
randint = random.randint(1, 90)
user = "user" + str(randint)
password = "password" + str(randint)
print(user, password)


def getsocket():
    # 实例化一个socket对象，指明协议
    datasocket = socket(AF_INET, SOCK_STREAM)
    # 连接服务端socket
    datasocket.connect((ip, server_port))
    return datasocket


def getsocket_ssl():
    # 实例化一个socket对象，指明协议
    datasocket = socket(AF_INET, SOCK_STREAM)
    # 连接服务端socket
    datasocket.connect((ip, server_port))
    # 生成SSL上下文
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # 不严重服务器域名
    context.check_hostname = False
    # 加载信任根证书
    context.load_verify_locations('CA2/server.crt')

    datasocket = context.wrap_socket(datasocket, server_side=False)

    return datasocket


def check():
    if use_ssl:
        datasocket = getsocket_ssl()
    else:
        datasocket = getsocket()
    # 用户验证
    if val(datasocket, user, password):
        print("login！")
        pass
    else:
        print("refuse！")
        return
    return datasocket


# 上传gps信息
def gps():
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()
    info = "gps"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    # recved = recved.decode("utf-8", "ignore")
    print(recved)
    if recved == b"yes":
        while True:
            # 从终端读入用户输入的字符串
            tosend = input('>>> ')
            if tosend == 'exit':
                datasocket.send(tosend.encode())
                print(tosend)
                break
            # 发送消息，也要编码为 bytes
            datasocket.send(tosend.encode())

            # 等待接收服务端的消息
            recved = datasocket.recv(buflen)
            # 如果返回空bytes，表示对方关闭了连接
            if not recved:
                break
            # 打印读取的信息
            print(recved.decode())

    datasocket.close()


# 短包信息
def short():
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()
    info = "short"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    # recved = recved.decode("utf-8", "ignore")
    print(recved)
    if recved == b"yes":
        datasocket.send("start".encode())
        while True:
            # 等待接收服务端的消息
            recved = datasocket.recv(buflen)
            # # 如果返回空bytes，表示对方关闭了连接
            # if not recved:
            #     break
            if recved == b'end':
                print("end")
                break
            datasocket.send(recved)
            # 打印读取的信息
            print(recved.decode())

    datasocket.close()


# 获取指定文件
def get_file_name(name):
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()
    start_t = time.time()

    info = "file"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    # recved = recved.decode("utf-8", "ignore")
    print(recved)
    base_path = "weights_c"
    if not os.path.isdir(base_path):
        os.makedirs(base_path)

    if recved == b"yes":
        file_name = name
        path = os.path.join(base_path, file_name)
        datasocket.send(file_name.encode())
        # 等待接收服务端的消息
        recved = datasocket.recv(buflen)
        if recved == b"start":

            with open(path, "wb") as f:
                while True:

                    recved = datasocket.recv(buflen)
                    # 如果返回空doned，表示完成文件传输
                    # print(recved)
                    # if recved == b"doned" or recved == b'':
                    if recved.endswith(b"doned") or recved == b'':
                        print("got file！")
                        break

                    f.write(recved)

    datasocket.close()
    print("download {} size={:.2f}M totaltime={:.2f}s"
          .format(path, os.path.getsize(path) / 1024. / 1024.,
                  time.time() - start_t))


# 获取文件
def get_file():
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()
    start_t = time.time()

    info = "send_file"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    # recved = recved.decode("utf-8", "ignore")
    print(recved)
    base_path = "file_c_ssl"
    if not os.path.isdir(base_path):
        os.makedirs(base_path)

    if recved == b"yes":
        datasocket.send("ok".encode())
        file_name = datasocket.recv(buflen).decode()
        path = os.path.join(base_path, file_name)
        datasocket.send(file_name.encode())
        # 等待接收服务端的消息
        recved = datasocket.recv(buflen)
        if recved == b"start":

            with open(path, "wb") as f:
                while True:

                    recved = datasocket.recv(buflen)
                    # 如果返回空doned，表示完成文件传输
                    # print(recved)
                    # if recved == b"doned" or recved == b'':
                    if recved.endswith(b"doned") or recved == b'':
                        print("got file！")
                        break

                    f.write(recved)

    datasocket.close()
    print("download {} size={:.2f}M totaltime={:.2f}s"
          .format(path, os.path.getsize(path) / 1024. / 1024.,
                  time.time() - start_t))


# 上传用户违规记录
def upload_record():
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()
    info = "record"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    print(recved)
    if recved == b"yes":
        info = "ready"
        datasocket.send(info.encode())
        # 等待接收服务端的消息
        recved = datasocket.recv(buflen)
        base_path = "./record"
        if not os.path.isdir(base_path):
            os.makedirs(base_path)
        if recved != b"":
            img_name = recved.decode("utf-8", "ignore")
            if img_name == "all":
                new_dirs = os.listdir(base_path)
            else:
                # print(img_name)
                file_name = os.path.splitext(img_name)
                # print(file_name)
                date = file_name[0].split("_")
                # print(date)
                dirs = os.listdir(base_path)
                # print(dirs)
                new_dirs = list(filter(lambda x: x >= date[0], dirs))
            new_dirs.sort()
            print(new_dirs)
            for nd in new_dirs:
                dir_path = os.path.join(base_path, nd)
                if img_name == "all":
                    new_imgs = os.listdir(dir_path)
                else:
                    imgs = os.listdir(dir_path)
                    # print(imgs)
                    new_imgs = list(filter(lambda x: x > img_name, imgs))
                new_imgs.sort()
                print(new_imgs)
                if len(new_imgs) > 0:
                    # datasocket.send("dir".encode())
                    # recved = datasocket.recv(buflen)
                    # if recved == b"yes":
                    #     datasocket.send(nd.encode())
                    #     recved = datasocket.recv(buflen)
                    #     if recved == b"start_dir":
                    #         for i in new_imgs:
                    #             datasocket.send(i.encode())
                    #             recved = datasocket.recv(buflen)
                    #             if recved == b"start_img":
                    #                 img_path = os.path.join(dir_path, i)
                    #                 with open(img_path, "rb") as f:
                    #                     # for data in f:
                    #                     #     datasocket.send(data)
                    #                     #     # print(data)
                    #                     while True:
                    #                         data = f.read(buflen)
                    #                         if len(data) == 0:
                    #                             break
                    #                         datasocket.send(data)
                    #                     print("doned")
                    #                 datasocket.send("doned".encode())
                    #                 # 注意两端交互顺序，可以多次发送，避免多次发送数据何在一起被接收，需等待回复
                    #                 recved = datasocket.recv(buflen)
                    #                 if recved == b"doned":
                    #                     pass
                    #         datasocket.send("dir_finished".encode())
                    #         # 注意两端交互顺序，可以多次发送，避免多次发送数据何在一起被接收，需等待回复
                    #         recved = datasocket.recv(buflen)
                    #         if recved == b"dir_finished":
                    #             pass
                    send_imgs(datasocket, nd, dir_path, new_imgs)
    datasocket.close()


def send_imgs(datasocket, nd, dir_path, new_imgs):
    datasocket.send("dir".encode())
    recved = datasocket.recv(buflen)
    if recved == b"yes":
        datasocket.send(nd.encode())
        recved = datasocket.recv(buflen)
        if recved == b"start_dir":
            for i in new_imgs:
                datasocket.send(i.encode())
                recved = datasocket.recv(buflen)
                if recved == b"start_img":
                    img_path = os.path.join(dir_path, i)
                    with open(img_path, "rb") as f:
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
                    # 注意两端交互顺序，可以多次发送，避免多次发送数据何在一起被接收，需等待回复
                    recved = datasocket.recv(buflen)
                    if recved == b"doned":
                        pass
            datasocket.send("dir_finished".encode())
            # 注意两端交互顺序，可以多次发送，避免多次发送数据何在一起被接收，需等待回复
            recved = datasocket.recv(buflen)
            if recved == b"dir_finished":
                pass


# 更新权重
def update_weight():
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()

    start_t = time.time()
    info = "update"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    # recved = recved.decode("utf-8", "ignore")
    weight_path = "./versions_c_ssl"
    print(recved)
    if recved == b"yes":
        versions = os.listdir(weight_path)
        filename = "empty"
        if len(versions) > 0:
            versions.sort(key=lambda x: x.split("_")[1])
            filename = versions[-1]
        print(filename)
        datasocket.send(filename.encode())
        # 等待接收服务端的消息
        recved = datasocket.recv(buflen)
        recved = recved.decode("utf-8", "ignore")
        if recved == "newest":
            print("You are already the latest version!")
        else:
            new_file = recved
            path = os.path.join(weight_path, new_file)
            print(path)
            with open(path, "wb") as f:
                while True:

                    recved = datasocket.recv(buflen)
                    # 如果返回空doned，表示完成文件传输
                    # print(recved)
                    # if recved == b"doned" or recved == b'':
                    if recved.endswith(b"doned") or recved == b'':
                        print("got {}".format(new_file))
                        break

                    f.write(recved)
            print("download {} size={:.2f}M totaltime={:.2f}s"
                  .format(path, os.path.getsize(path) / 1024. / 1024.,
                          time.time() - start_t))
    datasocket.close()


def val(socket, user, pwd):
    info = "{} {}".format(user, pwd)
    socket.send(info.encode())
    recved = socket.recv(buflen)
    if recved == b"pass":
        return True
    else:
        return False


# 获取服务端命令
def get_notice():
    # if use_ssl:
    #     datasocket = getsocket_ssl()
    # else:
    #     datasocket = getsocket()
    # # 用户验证
    # if val(datasocket, user, password):
    #     print("login！")
    #     pass
    # else:
    #     print("refuse！")
    #     return
    datasocket = check()
    info = "cmd"
    datasocket.send(info.encode())
    # 等待接收服务端的消息
    recved = datasocket.recv(buflen)
    # recved = recved.decode("utf-8", "ignore")
    print(recved)
    if recved == b"yes":
        datasocket.send("ready".encode())
        while True:
            # recved = datasocket.recv(buflen)
            # recved = recved.decode("utf-8", "ignore")
            # if recved == "upload_record":
            #     info = "upload_record"
            #     datasocket.send(info.encode())
            #     th = Thread(target=upload_record, args=())
            #     th.start()
            #     print(recved)
            # elif recved == "update_weight":
            #     info = "update_weight"
            #     datasocket.send(info.encode())
            #     th = Thread(target=update_weight, args=())
            #     th.start()
            #     print(recved)
            # elif recved == "send_file":
            #     info = "send_file"
            #     datasocket.send(info.encode())
            #     th = Thread(target=get_file, args=())
            #     th.start()
            #     print(recved)
            # elif recved == "get_file":
            #     info = "get_file"
            #     datasocket.send(info.encode())
            #     th = Thread(target=get_file_name, args=())
            #     th.start()
            #     print(recved)
            # elif recved == "gps":
            #     info = "gps"
            #     datasocket.send(info.encode())
            #     th = Thread(target=gps, args=())
            #     th.start()
            #     print(recved)
            # elif recved == "short":
            #     info = "short"
            #     datasocket.send(info.encode())
            #     th = Thread(target=short, args=())
            #     th.start()
            #     print(recved)
            # else:
            #     datasocket.send(recved.encode())
            #     print("say:", recved)
            create_message(datasocket)
    datasocket.close()


def create_message(datasocket):
    recved = datasocket.recv(buflen)
    recved = recved.decode("utf-8", "ignore")
    if recved == "upload_record":
        info = "upload_record"
        datasocket.send(info.encode())
        th = Thread(target=upload_record, args=())
        th.start()
        print(recved)
    elif recved == "update_weight":
        info = "update_weight"
        datasocket.send(info.encode())
        th = Thread(target=update_weight, args=())
        th.start()
        print(recved)
    elif recved == "send_file":
        info = "send_file"
        datasocket.send(info.encode())
        th = Thread(target=get_file, args=())
        th.start()
        print(recved)
    elif recved == "get_file":
        info = "get_file"
        datasocket.send(info.encode())
        th = Thread(target=get_file_name, args=())
        th.start()
        print(recved)
    elif recved == "gps":
        info = "gps"
        datasocket.send(info.encode())
        th = Thread(target=gps, args=())
        th.start()
        print(recved)
    elif recved == "short":
        info = "short"
        datasocket.send(info.encode())
        th = Thread(target=short, args=())
        th.start()
        print(recved)
    else:
        datasocket.send(recved.encode())
        print("say:", recved)


if __name__ == '__main__':
    # gps()
    # get_file()
    # update_weight()
    get_notice()
    # upload_record()
