import socket,os,filemanager
from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil
from PyQt5.QtWidgets import *
import pickle,sys,threading,test
device = ['This PC']
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_ip = '127.0.0.1'#or'localhost'
#sock_ip = socket.gethostname()
sock_port = 9009
sock.bind((sock_ip,sock_port))
sock.listen(10)
def looprecv():
    try:
        while True:
            recieve = c.recv(4046)
            try:
                recieve1 = pickle.loads(recieve)
            except:
                while True:
                    print(recieve)
                    ui.file.write(recieve)
                    recieve = c.recv(4046)
                    try:
                        recieve1 = pickle.loads(recieve)
                        break
                    except:
                        pass
                if ui.file.closed == False:
                    ui.file.close()

            if recieve1[0] == 'server : ' + str(sock_ip):
                if recieve1[-1] == 'Delete':
                    ui.Delete_for_otherDevice(recieve1)
                if recieve1[-1] == 'request':
                    ui.send_directory(recieve1)
                if recieve1[-1] == 'order':
                    ui.recieve_directory(recieve1)
                if recieve1[-1] == 'cut'and recieve1[2] != recieve1[3]:
                    ui.cut_for_otherDevice(recieve1)
                if recieve1[-1] == 'NewFolder':
                    ui.NewFolder_for_otherDevice(recieve1)
                if recieve1[-1] == 'Download_Message':
                    file = open(recieve1[-2],'rb')
                    read = file.read()
                    while True:
                        c.send(read)
                        read = file.read()
                        if not read:
                            break
                    file.close()
                if recieve1[-1] == 'chat':
                    itm = QtWidgets.QListWidgetItem()
                    itm.setText(recieve1[-3]+' :: '+recieve1[-2])
                    ui.chatroom.addItem(itm)
                    ui.lineEdit2.clear()
                if recieve1[-1] == 'send':

                    if ui.file_or_folder(recieve1[-2]) == 'File':
                        ui.file = open(ui.download_place+'\\'+recieve1[-2],'wb')
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