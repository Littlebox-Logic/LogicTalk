#!/usr/bin/python3
# -*- coding:utf-8 -*-

LOCALHOST = 'localhost'
PORT = 19130

import socketserver
import socket
import json
import pickle
from os import mknod, _exit
from hashlib import md5
from os.path import exists
import time

onlineu = []
userstr = ""

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
        except ConnectionResetError:
            self.reset()
        conn.sendall(bytes("[验证已收到] " + ret, encoding='utf-8'))
        try:
            if tuple(eval(ret))[0] == "login":
                try:
                    with open("user.pkl", 'rb') as f:
                        user = pickle.load(f)
                except:
                    print("<导入失败> 登录 %s\n... " % str(self.client_address)[1:-1], end = '')
        except:
            pass
                #conn.sendall(bytes("LoginFail", encoding='utf-8'))
                #break
            try:    
                if tuple(eval(ret))[0] == "login" and user[tuple(eval(ret))[1]] == tuple(eval(ret))[2]:
                    onlineu += user[tuple(eval(ret))[1]]
                    userstr += user[tuple(eval(ret))[1]]
                    userstr += '\n'
                    conn.sendall(bytes("在线用户:\n%s... " % userstr, encoding='utf-8'))
                    print("<在线信息> 已发送 %s\n... " % str(self.client_address)[1:-1], end = '')
                    print("[已发送] 在线用户:\n[已发送] %s... \n... " % userstr, end = '')
            except:
                print("<验证异常> %s\n... " % str(self.client_address)[1:-1], end = '')
        else:
            pass
        while True:
            ret = str(conn.recv(4096), encoding='utf-8')
            if ret == '("stop", -1)':
                break
            else:
                try:
                    if ret != '':
                        conn.sendall(bytes("[已收到] " + ret, encoding='utf-8'))
                        print("[已收到]-<%s> %s\n... " % (str(self.client_address)[1:-1], ret), end = "")
                        # md5(ret.encode(encoding='UTF-8')).hexdigest()
                except:
                    print("<传输断开> %s\n... " % str(self.client_address)[1:-1], end = '')
                    break

    def setup(self):
        global userstr
        print("[客户端] %s\n... " % str(self.client_address)[1:-1], end = '')
        for i in onlineu:
            userstr += i
            userstr += '\n'

    def finish(self):
        print("<连接结束> %s\n... " % str(self.client_address)[1:-1], end = '')

if __name__ == '__main__':
    print("\nLogic Talk\nVersion: 0.1.0 (Pre-alpha)\nCopyright (c) 2021 LittleBox Inc.\n\n 当前服务器:%s\n\n 服务器已启动...\n\n... " % get_host_ip(), end ="")

    time_start=time.time()
    while True:
        try:
            server = socketserver.ThreadingTCPServer((LOCALHOST, PORT), Server)
        except:
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
    print("<错误> %s\n..." % reason, end = '')
