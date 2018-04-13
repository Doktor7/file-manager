import socket,os,filemanager
from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil
from PyQt5.QtWidgets import *
import pickle,sys,threading
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_ip = '127.0.0.1'#or'localhost'
sock_port = 9009
sock.connect((sock_ip,sock_port))
avalable_device = [str(i) for i in pickle.loads(sock.recv(1024))]
if 'client : '+str(sock.getsockname()[1]) in avalable_device:
    avalable_device.remove('client : '+str(sock.getsockname()[1]))
avalable_device.insert(1,'server : '+str(sock_ip))
def show():
    global ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = filemanager.Ui_MainWindow(sock)
    ui.sockName = 'client : '+str(sock.getsockname()[1])
    ui.connected_name = 'server : '+str(sock_ip)
    ui.available_Device = avalable_device[:]
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def recvloop():
    data = []
    try:
        while True:
            recieve = sock.recv(4046)
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
            if recieve[0] == 'client : ' + str(sock.getsockname()[1]):
                if recieve[-1] == 'Delete':
                    ui.Delete_for_otherDevice(recieve)
                if recieve[-1] == 'request':
                    ui.send_directory(recieve)
                if recieve[-1] == 'order':
                    ui.recieve_directory(recieve)
                if recieve[-1] == 'cut' and recieve[2] != recieve[3]:
                    ui.cut_for_otherDevice(recieve)
                if recieve[-1] == 'NewFolder':
                    ui.NewFolder_for_otherDevice(recieve)
                if recieve[-1] == 'Download_Message':
                    ui.reply_Download(recieve)
                if recieve[-1] == 'chat':
                    ui.Thread_chat(recieve)
                if recieve[-1] == 'send':
                    ui.file = open(ui.download_place + '\\' + recieve[-2] , 'wb')
                if recieve[-1] == 'rename':
                    ui.reply_rename(recieve)

    except:
        pass

t2 = threading.Thread(target=show)
t1 = threading.Thread(target=recvloop)
t1.start()
t2.start()