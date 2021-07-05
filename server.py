#!/usr/bin/python3
# -*- coding:utf-8 -*-

HOSTNAME = 'localhost'
PORT = 19130

import socketserver
import socket
import json
import pickle
from os import mknod, _exit
from os.path import exists
from datetime import datetime
from re import compile
import time

onlineu = []
userstr = ""

# 匹配无端口号IP
clientip = compile(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])')
# 匹配有端口号IP
clientipport = compile(r"((?:(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d))\.){3}(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d)))")
# 留作备用

try:
    if not exists("users.pkl"):
        mknod("user.pkl")
except:
    pass

try:
    with open("user.pkl", 'rb') as f:
        user = pickle.load(f)
except:
    user = {}

user["logic"] = "070808"
pass

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
	    ip = "127.0.0.1"
    finally:
        s.close()

    return ip
    #return "127.0.0.1"

class Server(socketserver.BaseRequestHandler):
    islogin = False
    def handle(self):
        global user, onlineu, userstr
        conn = self.request
        conn.sendall(bytes("\nLogic Talk\nVersion: 0.1.0 (Pre-alpha)\nCopyright (c) 2021 LittleBox Inc.\n\n 已连接到服务器:%s\n 按q结束连接\n\n" % get_host_ip(), encoding='utf-8'))
        try:
            ret = str(conn.recv(64), encoding='utf-8')
            if ret == '':
                ret = "空验证"
            print("<收到验证> %s 验证: %s\n... " % (str(self.client_address)[1:-1], ret), end = '')  
            if ret == "<2, ClientType: C>":
                print("<连接类型> %s 来自C语言客户端的连接\n... " % str(self.client_address)[1:-1], end = '') 
            conn.sendall(bytes("[验证已收到] " + ret, encoding='utf-8'))
        except ConnectionResetError:
            print("<连接重置> %s\n... " % str(self.client_address)[1:-1], end = '')
            # conn.reset()
        try:
            if tuple(eval(ret))[0] == "login":
                try:
                    with open("user.pkl", 'rb') as f:
                        user = pickle.load(f)
                except:
                    print("<导入失败> 登  录 %s\n... " % str(self.client_address)[1:-1], end = '')
                else:
                    print("<记录导入> 登  录 %s\n... " % str(self.client_address)[1:-1], end = '')
        except:
            pass
                #conn.sendall(bytes("LoginFail", encoding='utf-8'))
                #break
        finally:
            try:    
                if tuple(eval(ret))[0] == "login" and user[tuple(eval(ret))[1]] == tuple(eval(ret))[2]:
                    onlineu += user[tuple(eval(ret))[1]]
                    userstr += user[tuple(eval(ret))[1]].replace('\n', '')
                    userstr += '\n'
                    conn.sendall(bytes("\n在线用户:\n%s... " % userstr, encoding='utf-8'))
                    print("<在线信息> 已发送 %s\n... " % str(self.client_address)[1:-1], end = '')
                    print("[信息发送] 在线用户:\n├──>[信息发送] %s└──>[信息发送] ... \n... " % userstr, end = '')
            except:
                pass

        while True:
            ret = str(conn.recv(4096), encoding='utf-8')
            if ret == '("stop", -1)':
                break
            elif ret == 'helo':
                conn.sendall(bytes("<Code: 200 OK >", encoding = 'utf-8'))
                print("<Returned: \"200 OK\" to \"HELO\"> %s\n... " % str(self.client_address)[1:-1], end = '')
            else:
                try:
                    if ret != '':
                        conn.sendall(bytes("[传输收到] " + ret, encoding = 'utf-8'))
                        print("[传输收到] %s 信息: %s\n... " % (str(self.client_address)[1:-1], ret), end = "")
                except:
                    print("<传输断开> %s\n... " % str(self.client_address)[1:-1], end = '')
                    break

    def setup(self):
        global userstr
        print("[用户连接] %s\n... " % str(self.client_address)[1:-1], end = '')
        temp = ""
        for i in onlineu:
            temp += i
        userstr += temp.replace('\n', '')
        userstr += '\n'
        temp = ""

    def finish(self):
        print("<连接结束> %s\n... " % str(self.client_address)[1:-1], end = '')

if __name__ == '__main__':
    if int(datetime.now().strftime('%H')) < 6:
        hello = "Early hours of the new day, 加班有度, 减少劳累吧..."
    elif int(datetime.now().strftime('%H')) < 11:
        hello = "Good morning, 早上好, 煮一杯咖啡吧(๑´0`๑)"
    elif int(datetime.now().strftime('%H')) < 14:
        hello = "It's noon, 借一盏茶意, 休息一下吧(◦˙▽˙◦)"
    elif int(datetime.now().strftime('%H')) < 18:
        hello = "Good afternoon, 下午工作努力哦⊙∀⊙!"
    elif int(datetime.now().strftime('%H')) < 21:
        hello = "Hi, evening, 晚风吹过好时光..."
    else:
        hello = "Night, sleep, 带着一天的困倦拥抱明天..."

    print("\nLogic Talk\nVersion: 0.1.0 (Pre-alpha)\nCopyright (c) 2021 LittleBox Inc.\n\n 当前服务器:%s\n\n 服务器已启动...\n\n %s\n %s\n\n... " % (get_host_ip() + ':' + str(PORT), datetime.now().strftime('%Y.%m.%d (%a) %H:%M:%S %Z'), hello), end ="")

    time_start=time.time()
    while True:
        try:
            server = socketserver.ThreadingTCPServer((HOSTNAME, PORT), Server)
        except:
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                _exit(0)
            print("<启动失败> 正在尝试重新启动...\n... ", end = '')
        else:
            break
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n%s\n<服务器已终止> " % ('_' * 25), end = '')

    time_end=time.time()
    print("运行时间: %s Sec\n" % str(time_end-time_start))
    server.shutdown()
    _exit(0)
except Exception as reason:
    print("<未知错误> %s\n..." % reason, end = '')
