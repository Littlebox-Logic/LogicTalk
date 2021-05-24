#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket

IP = "192.168.1.101"
port = 19130

client_sk = socket.socket()
client_sk.connect((IP, port))

print(str(client_sk.recv(1024), encoding='utf-8'))
while True:
    inp = input("<待传输> : ")
    if inp == "login":
        client_sk.sendall(bytes(str(("login", "logic", "070808")), encoding='utf-8'))
        print(str(client_sk.recv(1024)))
    else:
        client_sk.sendall(bytes(inp, encoding='utf-8'))
    if inp == 'q':
        client_sk.sendall(bytes("(\"stop\", -1)", encoding='utf-8'))
        break
    else:
        print(str(client_sk.recv(1024), encoding='utf-8'))

client_sk.close()
