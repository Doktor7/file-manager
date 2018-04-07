from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil
from PyQt5.QtWidgets import *
import pickle,socket,threading
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 350
        self.top = 140
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)

class Ui_MainWindow(object):
    def __init__(self,sock):
        self.download_place = '\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Downloads'
        self.file = None
        self.Download_Message = []
        self.send_message = []
        self.cut_message = []
        self.NewFolder_Message = []
        self.sockName = ''
        self.connected_name = ''
        self.accessed_device = False
        self.sock = sock
        self.available_Folders = []
        self.available_Drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        self.File_Cut = ''
        self.File_Copy = ''
        self.File_name_Cut = []
        self.File_name_Copy =[]
    def set_icon(self, file, icon):
        self.Formats = ['pdf', 'mp3', 'jpg', 'aac', 'avi', 'bmp', 'chm', 'css', 'defult', 'dll', 'doc', 'docx', \
                        'fla', 'htm', 'html', 'ini', 'jar', 'jpeg', 'js', 'lasso', 'mdp', 'mov', 'mp4', 'mpg', \
                        'ogg', 'ogv', 'php', 'png', 'ppt', 'py', 'rb', 'real', 'reg', 'rtf', 'sgl', 'swf', 'txt', \
                        'vbs', 'wav', 'webm', 'wmv', 'xls', 'xlsx', 'xml', 'xsl', 'zip', 'rar', 'mkv', 'exe', 'srt',
                        '3gp', 'log', 'ico']
        for format in self.Formats:
            if self.available_Folders[file].endswith(format):
                icon.addPixmap(QtGui.QPixmap(format), QtGui.QIcon.Normal, QtGui.QIcon.On)
    def change_item_listwidget(self, list):
        for i in range(len(self.available_Folders)):
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            if str(self.available_Folders[i]).find(':') != -1:
                icon.addPixmap(QtGui.QPixmap('drive icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            else:
                icon.addPixmap(QtGui.QPixmap('_Close.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.set_icon(i, icon)
            item.setIcon(icon)
            item.setText(str(self.available_Folders[i]))
            self.listWidget.addItem(item)

    def setupUi(self, MainWindow):
        self.address_bar = ''
        self.path = []
        self.opening_lst = []
        self.path2 = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 500, 540))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget.setObjectName("ListWidget")
        self.chatroom = QtWidgets.QListWidget(self.centralwidget)
        self.chatroom.setObjectName("chat")
        self.chatroom.setGeometry(QtCore.QRect(500,0,500 , 600))
        self.available_Folders = self.available_Device[:]
        self.change_item_listwidget(self.available_Folders)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.lineEdit2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit2.setObjectName("lineEdit2")
        self.gridLayout.addWidget(self.lineEdit2, 600, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.listWidget.itemDoubleClicked.connect(self.selecticoncange)
        self.listWidget.itemClicked.connect(self.selected)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 615, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionEdit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon)
        self.actionEdit.setObjectName("actionEdit")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon1)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon2)
        self.actionCut.setObjectName("actionCut")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon3)
        self.actionDelete.setObjectName("actionDelete")
        self.actionForward = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionForward.setIcon(icon4)
        self.actionForward.setObjectName("actionForward")
        self.actionchat = QtWidgets.QAction(MainWindow)
        self.actionchat.setObjectName("actionchat")
        self.actionEdit_2 = QtWidgets.QAction(MainWindow)
        self.actionEdit_2.setIcon(icon)
        self.actionEdit_2.setObjectName("actionEdit_2")
        self.actionPaste_2 = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste_2.setIcon(icon5)
        self.actionPaste_2.setObjectName("actionPaste_2")
        self.actionDownload = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDownload.setIcon(icon6)
        self.actionDownload.setObjectName("actionDownload")
        self.actionSend = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("Send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSend.setIcon(icon9)
        self.actionSend.setObjectName("actionSend")
        self.actionCopy_2 = QtWidgets.QAction(MainWindow)
        self.actionCopy_2.setIcon(icon1)
        self.actionCopy_2.setObjectName("actionCopy_2")
        self.actionBackward = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackward.setIcon(icon7)
        self.actionBackward.setObjectName("actionBackward")
        self.actionNew_Folder = QtWidgets.QAction(MainWindow)
        self.actionNew_Folder.setObjectName("actionNew_Folder")
        self.actionCut_3 = QtWidgets.QAction(MainWindow)
        self.actionCut_3.setIcon(icon2)
        self.actionCut_3.setObjectName("actionCut_3")
        self.actionDelete_2 = QtWidgets.QAction(MainWindow)
        self.actionDelete_2.setIcon(icon3)
        self.actionDelete_2.setObjectName("actionDelete_2")
        self.actionRename_2 = QtWidgets.QAction(MainWindow)
        self.actionRename_2.setObjectName("actionRename_2")
        self.actionCompress_2 = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("zip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCompress_2.setIcon(icon8)
        self.actionCompress_2.setObjectName("actionCompress_2")
        self.actionExit_2 = QtWidgets.QAction(MainWindow)
        self.actionExit_2.setObjectName("actionExit_2")
        self.actionCopy_3 = QtWidgets.QAction(MainWindow)
        self.actionCopy_3.setIcon(icon1)
        self.actionCopy_3.setObjectName("actionCopy_3")
        self.actionCut_4 = QtWidgets.QAction(MainWindow)
        self.actionCut_4.setIcon(icon2)
        self.actionCut_4.setObjectName("actionCut_4")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setIcon(icon5)
        self.actionPaste.setObjectName("actionPaste")
        self.menuFile.addAction(self.actionCopy)
        self.menuFile.addAction(self.actionEdit_2)
        self.menuFile.addAction(self.actionCut_3)
        self.menuFile.addAction(self.actionDelete_2)
        self.menuFile.addAction(self.actionRename_2)
        self.menuFile.addAction(self.actionCompress_2)
        self.menuFile.addAction(self.actionExit_2)
        self.menuEdit.addAction(self.actionNew_Folder)
        self.menuEdit.addAction(self.actionCopy_3)
        self.menuEdit.addAction(self.actionCut_4)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionchat)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionPaste_2)
        self.toolBar.addAction(self.actionDownload)
        self.toolBar.addAction(self.actionSend)
        self.toolBar.addAction(self.actionCopy_2)
        self.toolBar.addAction(self.actionForward)
        # self.toolBar.addAction(self.actionchat)
        self.toolBar.addAction(self.actionBackward)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionEdit.setText(_translate("MainWindow", "Edit"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionForward.setText(_translate("MainWindow", "Forward"))
        self.actionchat.setText(_translate("MainWindow", "chat"))
        self.actionEdit_2.setText(_translate("MainWindow", "Edit"))
        self.actionEdit_2.setToolTip(_translate("MainWindow", "Edit"))
        self.actionPaste_2.setText(_translate("MainWindow", "Paste"))
        self.actionDownload.setText(_translate("MainWindow", "Download"))
        self.actionSend.setText(_translate("MainWindow", "Send"))
        self.actionCopy_2.setText(_translate("MainWindow", "Copy"))
        self.actionBackward.setText(_translate("MainWindow", "Backward"))
        self.actionNew_Folder.setText(_translate("MainWindow", "New Folder"))
        self.actionCut_3.setText(_translate("MainWindow", "Cut"))
        self.actionDelete_2.setText(_translate("MainWindow", "Delete"))
        self.actionRename_2.setText(_translate("MainWindow", "Rename"))
        self.actionCompress_2.setText(_translate("MainWindow", "compress"))
        self.actionExit_2.setText(_translate("MainWindow", "Exit"))
        self.actionCopy_3.setText(_translate("MainWindow", "Copy"))
        self.actionCut_4.setText(_translate("MainWindow", "Cut"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionNew_Folder.setShortcut('Ctrl+N')
        self.actionBackward.setShortcut('BackSpace')
        self.actionExit_2.setShortcut('Ctrl+Q')
        self.actionDelete.setShortcut('Shift+Delete')
        self.actionForward.setShortcut('Tab')
        self.actionEdit_2.setShortcut('Ctrl+E')
        self.actionCopy.setShortcut('Ctrl+C')
        self.actionPaste.setShortcut('Ctrl+V')
        self.actionCut_3.setShortcut('Ctrl+X')
        self.actionRename_2.setShortcut('Ctrl+R')
        self.actionDownload.setShortcut('Ctrl+D')
        self.actionSend.setShortcut('Ctrl+S')
        self.actionchat.setShortcut('Ctrl+P')
        self.actionForward.triggered.connect(self.Forward)
        self.actionBackward.triggered.connect(self.Backward)
        self.actionNew_Folder.triggered.connect(self.add_New_Folder)
        self.actionDelete.triggered.connect(self.delete)
        self.actionDelete_2.triggered.connect(self.delete)
        self.actionExit_2.triggered.connect(self.close)
        self.actionRename_2.triggered.connect(self.rename)
        self.actionEdit.triggered.connect(self.Edit)
        self.actionEdit_2.triggered.connect(self.Edit)
        self.actionCopy.triggered.connect(self.Copy)
        self.actionCopy_3.triggered.connect(self.Copy)
        self.actionCopy_2.triggered.connect(self.Copy)
        self.actionPaste.triggered.connect(self.Paste)
        self.actionPaste_2.triggered.connect(self.Paste)
        self.actionCut.triggered.connect(self.Cut)
        self.actionCut_3.triggered.connect(self.Cut)
        self.actionCut_4.triggered.connect(self.Cut)
        self.actionSend.triggered.connect(self.send)
        self.actionDownload.triggered.connect(self.Download)
        self.actionchat.triggered.connect(self.chat)
    def dir_list_folder(self, paths):
        for folderName in os.listdir(paths):
            if folderName != '$RECYCLE.BIN' and folderName != 'System Volume Information':
                self.available_Folders.append(folderName)

    def file_or_folder(self, text):
        flag = False
        for each_format in self.Formats:
            if text.endswith(each_format) == True:
                flag = True
        if flag == True:
            return 'File'
        else:
            return 'Folder'

    def selected(self):
        self.Filename = []
        for it in self.listWidget.selectedItems():
            self.Filename.append(it.text())

    def delete(self):
        if self.accessed_device == False and len(self.path)>1 and len(self.Filename)>0:
            self.question = App()
            buttonReply = QMessageBox.question(self.question, 'Delete File', "Are you sur you want to permanently delete this file??", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                if len(self.path)>1 and len(self.Filename)>0:
                    self.destiny = '\\'.join(self.path[1:])

                    if self.Filename[-1] != '...' and len(self.Filename) != 0:
                        try:
                            os.remove(self.destiny + '\\' + self.Filename[-1])
                        except:
                            shutil.rmtree(self.destiny + '\\' + self.Filename[-1])
                        if len(self.Filename) != 0:
                            try:
                                self.available_Folders.remove(str(self.Filename[-1]))
                                self.listWidget.clear()
                                self.change_item_listwidget(self.available_Folders)
                                self.Filename.remove(self.Filename[0])
                            except:
                                pass
            else:
                pass
        if self.accessed_device == True and len(self.path)>1 and len(self.Filename)>0:
            self.question = App()
            buttonReply = QMessageBox.question(self.question, 'Delete File', "Are you sur you want to permanently delete this file??", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.path.append(self.Filename[-1])
                self.Delete_message(self.path)
                self.path.remove(self.Filename[-1])
    def selecticoncange(self):
        self.available_Folders.clear()
        self.available_Folders.append('...')
        for currentitem in self.listWidget.selectedItems():
            self.path.append(currentitem.text())
            self.opening_lst.append(currentitem.text())
            if currentitem.text()!='This PC' and len(self.path)==1:
                self.accessed_device = True
            if currentitem.text() =='This PC' and len(self.path)==1:
                self.accessed_device = False
            if self.accessed_device == False:
                if currentitem.text() == '...' and len(self.path) == 2:
                    self.path.clear()
                    self.available_Folders = self.available_Device[:]
                elif currentitem.text() == '...' and len(self.path) == 3:
                    self.listWidget.clear()
                    del self.path[-1]
                    del self.path[-1]
                elif currentitem.text() == '...' and len(self.path) > 3:
                    del self.path[-1]
                    del self.path[-1]

                if len(self.path) == 1:
                    self.available_Folders = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
                    self.available_Folders.insert(0,'...')
                elif len(self.path) == 2:
                    self.dir_list_folder(self.path[1] + '\\')
                elif len(self.path) > 2:
                    if self.file_or_folder(currentitem.text()) == 'Folder':
                        self.dir_list_folder('\\'.join(self.path[1:]))
                    if self.file_or_folder(currentitem.text()) == 'File':
                        os.startfile('\\'.join(self.path[1:]))
            if self.accessed_device == True:
                if self.file_or_folder(currentitem.text()) == 'File':
                    self.path.remove(currentitem.text())
                if currentitem.text() == '...' and len(self.path) > 2:
                    del self.path[-1]
                    del self.path[-1]
                    self.request_message(self.path)
                elif currentitem.text() == '...' and len(self.path) == 2:
                    self.path.clear()
                    self.listWidget.clear()
                    self.available_Folders = self.available_Device[:]
                    self.change_item_listwidget(self.available_Folders)
                    self.lineEdit.setText('')

                else:
                    if self.file_or_folder(currentitem.text()) == 'Folder':
                        self.request_message(self.path)

            # if self.accessed_device == True:
        if self.accessed_device == False:
            if len(self.path) > 0:
                if self.file_or_folder(self.path[-1]) == 'Folder':
                    self.listWidget.clear()
                    self.lineEdit.setText(str('\\'.join(self.path)))
                if self.file_or_folder(self.path[-1]) == 'File':
                    del self.path[-1]
                    del self.available_Folders[-1]
            elif len(self.path) == 0 and len(self.path2) == 0:
                self.listWidget.clear()
                self.lineEdit.setText('')
            self.change_item_listwidget(self.available_Folders)


        self.Filename=[]
    def add_New_Folder(self):
        if self.accessed_device == False:
            if len(self.path)>1:
                First_Directory = os.getcwd()
                current_address = '\\'.join(self.path[1:])
                if len(current_address) != 0:
                    os.chdir(current_address)
                if os.path.isdir(current_address + '\\' + 'New Folder') == False:
                    os.mkdir('New Folder')
                    os.chdir(First_Directory)
                    self.available_Folders.append('New Folder')
                else:
                    th = 1
                    while os.path.isdir(current_address + '\\' + 'New Folder' + '(' + str(th) + ')') == True:
                        th += 1
                    os.mkdir('New Folder' + '(' + str(th) + ')')
                    os.chdir(First_Directory)
                    self.available_Folders.append('New Folder' + '(' + str(th) + ')')
                self.listWidget.clear()
                self.change_item_listwidget(self.available_Folders)
        if self.accessed_device == True and len(self.path)>1:
            current_address = '\\'.join(self.path[1:])
            self.NewFolder_Message.append(current_address)
            self.NewFolder_Message.insert(0,self.path[0])
            self.newFolder_Message(self.NewFolder_Message)


    def close(self):
        import sys
        sys.exit(app.exec_())

    def rename(self):
        if self.accessed_device == False:
            if len(self.path)>1 and len(self.Filename)>0:
                self.w = App()
                text, okPressed = QInputDialog.getText(self.w, "Rename", "Enetr New Name:", QLineEdit.Normal, "")
                if okPressed and text != '':
                    First = os.getcwd()

                    current = '\\'.join(self.path[1:])
                    if len(current) != 0:
                        os.chdir(current)
                    os.rename(self.Filename[-1], text)
                    os.chdir(First)
                    self.available_Folders.remove(str(self.Filename[-1]))
                    self.available_Folders.append(text)
                    self.listWidget.clear()
                    self.change_item_listwidget(self.available_Folders)
    def Forward(self):
        if self.accessed_device == False:
            if os.path.isdir(str(self.lineEdit.text())):
                self.available_Folders.clear()
                self.available_Folders.append('...')
                self.listWidget.clear()
                self.path = self.lineEdit.text().split('\\')
                self.dir_list_folder(self.lineEdit.text())
                self.change_item_listwidget(self.available_Folders)
            else:
                messagebox = QtWidgets.QMessageBox(MainWindow)
                messagebox.setWindowTitle('warning')
                messagebox.setText("windows can't find '"+str(self.lineEdit.text())+"' check the spelling and try again")
                messagebox.setStandardButtons(QMessageBox.Ok)
                messagebox.setIcon(QMessageBox.Warning)
                messagebox.show()

    def Backward(self):
        self.Filename =[]
        if len(self.path) == 2:
            self.listWidget.clear()
            del self.path[-1]
            self.available_Folders = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
            self.available_Folders.insert(0,'...')
            self.change_item_listwidget(self.available_Folders)
        elif len(self.path) > 2:
            self.available_Folders.clear()
            self.listWidget.clear()
            self.available_Folders.append('...')
            del self.path[-1]
            self.dir_list_folder('\\'.join(self.path[1:]))
            self.change_item_listwidget(self.available_Folders)
        elif len(self.path) == 1:
            self.listWidget.clear()
            self.path.clear()
            self.available_Folders = self.available_Device[:]
            self.change_item_listwidget(self.available_Folders)
        self.lineEdit.setText(str('\\'.join(self.path)))
    def Edit(self):
        os.startfile(shutil.which('Notepad'))

    def Copy(self):
        self.File_name_Cut = []
        if len(self.path) > 1 and self.Filename[-1] != '...'and self.accessed_device == False:
            self.File_name_Copy.append('\\'.join(self.path[1:]))
            self.File_name_Copy.append(self.Filename[-1])
            self.File_Copy = str('\\'.join(self.path[1:])) + '\\' + str(self.Filename[-1])
    def Cut(self):
        self.File_name_Copy = []
        if len(self.path) > 1 and self.Filename[-1] != '...' and len(self.Filename)>0:
            self.File_name_Cut.append('\\'.join(self.path[1:]))
            self.File_name_Cut.append(self.Filename[-1])
            self.File_Cut = str('\\'.join(self.path[1:])) + '\\' + str(self.Filename[-1])