#!/usr/bin/python3
# -*- coding:utf-8 -*-

LOCALHOST = 'localhost'
PORT = 19130

import socketserver
import socket
import json
import pickle
from os import mknod, _exit
from os.path import exists
from hashlib import md5
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
        ret = str(conn.recv(64), encoding='utf-8')
        #ret = md5(ret.encode(encoding='UTF-8')).hexdigest()
        conn.sendall(bytes("[验证已收到] " + ret, encoding='utf-8'))
        if tuple(eval(ret))[0] == "login":
            try:
                with open("user.pkl", 'rb') as f:
                    user = pickle.load(f)
            except:
                print("<导入失败> 登录 %s\n... " % str(self.client_address)[1:-1], end = '')
                #conn.sendall(bytes("LoginFail", encoding='utf-8'))
                #break
            if user[tuple(eval(ret))[1]] == tuple(eval(ret))[2]:
                onlineu += user[tuple(eval(ret))[1]]
                userstr += user[tuple(eval(ret))[1]]
                userstr += '\n'
                conn.sendall(bytes("在线用户:\n%s... " % userstr, encoding='utf-8'))
                print("<在线信息> 已发送 %s\n... " % str(self.client_address)[1:-1], end = '')
        else:
            pass
        while True:
            ret = str(conn.recv(4096), encoding='utf-8')
            if ret == '("stop", -1)':
                break
            else:
                try:
                    conn.sendall(bytes("[已收到] " + ret, encoding='utf-8'))
                    print("[已收到] %s\n... " % ret, end = "")
                except:
                    print("<传输断开> %s\n... " % str(self.client_address)[1:-1], end = '')
                    break

    def setup(self):
        print("[客户端] %s\n... " % str(self.client_address)[1:-1], end = '')
        for i in onlineu:
            userstr += i
            userstr += '\n'

    def finish(self):
        print("<连接结束> %s\n... " % str(self.client_address)[1:-1], end = '')

if __name__ == '__main__':
    print("\nLogic Talk\nVersion: 0.1.0 (Pre-alpha)\nCopyright (c) 2021 LittleBox Inc.\n\n 当前服务器:%s\n\n 服务器已启动...\n\n... " % get_host_ip(), end ="")

    time_start=time.time()
    server = socketserver.ThreadingTCPServer((LOCALHOST, PORT), Server)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n%s\n<服务器已终止> " % ('_' * 25), end = '')

    time_end=time.time()
    print("运行时间: %s Sec\n" % str(time_end-time_start))
    server.shutdown()
    _exit(0)
