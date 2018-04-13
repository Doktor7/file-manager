import socket,os,filemanager
from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil
from PyQt5.QtWidgets import *
import pickle,sys,threading,test
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

device = ['This PC']
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_ip = '127.0.0.1'#or'localhost'
#sock_ip = socket.gethostname()
sock_port = 9009
sock.bind((sock_ip,sock_port))
sock.listen(10)
def looprecv():
    data = []
    try:
        while True:
            recieve = c.recv(4046)
            if not recieve:
                ui.file.close()
                break
            data.append(recieve)
            if len(data) == 1:
                try:
                    recieve = pickle.loads(data[0])
                    data.clear()
                except:
                    print(recieve)
                    ui.file.write(data[0])
                    data.clear()
            if recieve[0] == 'server : ' + str(sock_ip):
                if recieve[-1] == 'Delete':
                    ui.Delete_for_otherDevice(recieve)
                elif recieve[-1] == 'request':
                    ui.send_directory(recieve)
                elif recieve[-1] == 'order':
                    ui.recieve_directory(recieve)
                elif recieve[-1] == 'cut'and recieve[2] != recieve[3]:
                    ui.cut_for_otherDevice(recieve)
                elif recieve[-1] == 'NewFolder':
                    ui.NewFolder_for_otherDevice(recieve)
                elif recieve[-1] == 'Download_Message':
                    ui.reply_Download(recieve)
                elif recieve[-1] == 'chat':
                    ui.Thread_chat(recieve)
                elif recieve[-1] == 'send':
                    ui.file = open(ui.download_place+'\\'+recieve[-2],'wb')
                elif recieve[-1] == 'rename':
                    ui.reply_rename(recieve)

    except:
        pass
def show():
    global ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = filemanager.Ui_MainWindow(c)
    ui.sockName = 'server : '+str(sock_ip)
    ui.connected_name = device[1]
    ui.available_Device = device[:]
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
t_recv = threading.Thread(target=looprecv)
t_main = threading.Thread(target=show)
while True:
    c,addr = sock.accept()
    device.append('client : '+str(addr[1]))
    c.send(pickle.dumps(device))

    t_recv.start()
    t_main.start()