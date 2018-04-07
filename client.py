import socket,os,filemanager
from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil
from PyQt5.QtWidgets import *
import pickle,sys,threading,test
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
t2 = threading.Thread(target=show)
t1 = threading.Thread(target=recvloop)
t1.start()
t2.start()