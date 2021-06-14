#!/usr/bin/python3
# -*- coding:utf-8 -*-

from tkinter import *
import socket, threading
from os import _exit
from threading import Thread

client_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
client_sk.connect(('localhost', 19130))

root = Tk()
root.title("LogicTalk")
root.geometry("600x450")
Label(text = " [服务器直连]       按q结束连接", justify = LEFT, anchor = 'w').grid(sticky = W, pady = 10, column = 0, row = 0)

getmain = Frame(root)
getmain.grid(column = 0, row = 1, columnspan = 2, sticky = W)
sbx = Scrollbar(getmain)
sbx.pack(side = BOTTOM, fill = X)
sby = Scrollbar(getmain)
sby.pack(side = RIGHT, fill = Y)
messages = Text(getmain, xscrollcommand = sbx.set, yscrollcommand = sby.set)
messages.pack()
sbx.config(command = messages.xview)
sby.config(command = messages.yview)
def get():
    global lines
    while True:
        try:
            ret = client_sk.recv(4096)
            if ret != '':
                messages.configure(state = "normal")
                messages.insert(END, str(ret, encoding='utf-8') + '\n')
                messages.configure(state = "disabled")
            else:
                pass
        except Exception as reason:
            messages.configure(state = "normal")
            messages.insert(END, '错误: %s\n' % str(reason))
            messages.configure(state = "disabled")

tget = Thread(target = get)
tget.start()

def post():
    inp = e.get()
    if inp == "login":
        client_sk.sendall(bytes(str(("login", "logic", "070808")), encoding='utf-8'))
    else:
        client_sk.sendall(bytes(inp, encoding='utf-8'))
        if inp == 'q':
            client_sk.sendall(bytes("(\"stop\", -1)", encoding='utf-8'))
            _exit(0)
    e.delete(0, END)

e = Entry(root)
e.place(relx = 0.5, rely = 0.99, anchor = S)

Button(master = root, text = " 发送 ", command = post).place(relx = 0.8, rely = 0)#.grid(column = 1, row = 0, sticky = W)
root.bind("<Key-Return>", lambda event : post())
mainloop()
