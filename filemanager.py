from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pickle,socket,threading,time
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 350
        self.top = 140
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
class Ui_MainWindow(QMainWindow,object):
    def __init__(self,sock):
        QMainWindow.__init__(self)
        self.hide_folder = ['$GetCurrent','$Recycle.Bin','AMTAG.BIN','Boot','bootmgr','BOOTNXT','BOOTSECT.BAK','Config.Msi',\
                            'Documents and Settings','hiberfil.sys','MSOCache','pagefile.sys','PerfLogs','ProgramData',\
                            'Recovery','swapfile.sys','$WINER_BACKUP_PARTITION.MARKER','System Volume Information','DRIVERS','$RECYCLE.BIN']
        self.download_place = '\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Downloads'
        self.file = None
        self.Download_Message = []
        self.send_message = []
        self.cut_message = []
        self.NewFolder_Message = []
        self.rename_message = []
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
            if 'client'in str(self.available_Folders[i]):
                icon.addPixmap(QtGui.QPixmap('client.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif 'server' in str(self.available_Folders[i]):
                icon.addPixmap(QtGui.QPixmap('server.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif 'This PC' in str(self.available_Folders[i]):
                icon.addPixmap(QtGui.QPixmap('This PC.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(self.available_Folders[i]).find(':') != -1:
                icon.addPixmap(QtGui.QPixmap('drive icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            else:
                icon.addPixmap(QtGui.QPixmap('_Close.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.set_icon(i, icon)
            item.setIcon(icon)
            font = QtGui.QFont()
            font.setFamily("Sitka Text")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setForeground(brush)
            item.setText(str(self.available_Folders[i]))
            self.listWidget.addItem(item)

    def setupUi(self, MainWindow):
        self.address_bar = ''
        self.path = []
        self.opening_lst = []
        self.path2 = []
        MainWindow.setObjectName("File Manager")
        MainWindow.resize(1350, 695)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(235, 0, 680, 620))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget.setIconSize(QtCore.QSize(40, 40))
        self.listWidget.setWordWrap(False)
        self.listWidget.setObjectName("ListWidget")
        self.listWidget.setStyleSheet("border-image: url(background-2.jpg);")
        self.chatroom = QtWidgets.QListWidget(self.centralwidget)
        self.chatroom.setObjectName("chat")
        self.chatroom.setStyleSheet("border-image: url(chat.jpg);")
        self.chatroom.setGeometry(QtCore.QRect(920,0,420 , 595))
        self.available_Folders = self.available_Device[:]
        self.change_item_listwidget(self.available_Folders)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit2.setGeometry(QtCore.QRect(920,600,421, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionchat = QtWidgets.QPushButton(self.centralwidget)
        self.actionchat.setGeometry(QtCore.QRect(1320, 600, 21, 21))
        self.actionchat.setStyleSheet("border-image: url(send message.png);")
        self.actionchat.setText("")
        self.actionchat.setObjectName("pushButton")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 475, 220, 145))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("border-image: url(thumbnail.jpg);")
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
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setIconSize(QtCore.QSize(40, 40))
        self.toolBar.setObjectName("toolBar")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 0, 220, 470))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setAnimated(True)
        self.treeWidget.setIndentation(20)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.itemClicked.connect(self.treeclick)
        self.treeWidget.setStyleSheet("border-image: url(background-2.jpg);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Quick-Access.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.treeWidget.headerItem().setIcon(0, icon)
        self.treeWidget.headerItem().setText(0,'Quick access')
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Desktop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon1)
        item_0.setText(0,'Desktop')
        self.show_directory(item_0, os.listdir('\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Desktop'),'\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Desktop\\')
        item_1 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("downlaods.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon2)
        item_1.setText(0,'Downloads')
        self.show_directory(item_1, os.listdir('\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Downloads'), '\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Downloads\\')
        item_2 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Document.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_2.setIcon(0, icon3)
        item_2.setText(0,'Documents')
        self.show_directory(item_2, os.listdir('\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Documents'), '\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Documents\\')
        item_3 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Pictures.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_3.setIcon(0, icon4)
        item_3.setText(0,'Pictures')
        self.show_directory(item_3, os.listdir('\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Pictures'), '\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Pictures\\')
        item_4 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Music.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_4.setIcon(0, icon5)
        item_4.setText(0,'Music')
        self.show_directory(item_4, os.listdir('\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Music'), '\\'.join(os.getcwd().split('\\')[0:3])+'\\'+'Music\\')
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
        self.actionchat.setShortcut('Return')
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
        self.actionchat.clicked.connect(self.chat)
    def treeclick(self):
        for c in self.treeWidget.selectedItems():
            if c.text(0) == 'Desktop'or c.text(0)=='Downloads'or c.text(0)=='Documents'or c.text(0)=='Music'or c.text(0)=='Pictures':
                self.accessed_device = False
                self.path.clear()
                self.path = ('\\'.join(os.getcwd().split('\\')[0:3])+'\\'+c.text(0)).split('\\')
                self.path.insert(0,'This PC')
                self.lineEdit.setText('This PC\\'+'\\'.join(self.path[1:]))
                self.listWidget.clear()
                self.available_Folders.clear()
                self.available_Folders.append('...')
                self.dir_list_folder('\\'.join(self.path[1:]))
                self.change_item_listwidget(self.available_Folders)
    def File_or_Folder(self, text):
        if '.' in text:
            return 'File'
        else:
            return 'Folder'
    def show_directory(self,item,list,path):
        for F in list:
            if F not in self.hide_folder:
                icon = QtGui.QIcon()
                pre_item = QtWidgets.QTreeWidgetItem()
                pre_item.setText(0,str(F))
                if self.File_or_Folder(F) == 'File':
                    for format in self.Formats:
                        if F.endswith(format):
                            icon.addPixmap(QtGui.QPixmap(format), QtGui.QIcon.Normal, QtGui.QIcon.On)
                            pre_item.setIcon(0, icon)

                item.addChild(pre_item)
                if self.File_or_Folder(F) == 'Folder':
                    icon.addPixmap(QtGui.QPixmap('_Close.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pre_item.setIcon(0,icon)
                    try:
                        os.listdir(path + str(F))
                        self.show_directory(pre_item,os.listdir(path+str(F)),path+str(F)+'\\')
                    except:
                        pass
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
        if self.Filename[0].endswith('jpg') and self.accessed_device == False:
            self.thumbnail(self.Filename[0])
        else:
            self.graphicsView.setStyleSheet("border-image: url(thumbnail.jpg);")
    def thumbnail(self,name):
        self.graphicsView.setStyleSheet("border-image: url("+'/'.join(self.path[1:])+'/'+name+");")
    def delete(self):
        if self.accessed_device == False and len(self.path)>1 and len(self.Filename)>0:
            self.question = App()
            buttonReply = QMessageBox.question(self.question, 'Delete File', "Are you sur you want to permanently delete this file??", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            print(buttonReply)
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
        self.Filename = []
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
        else:
            if len(self.path)>1 and len(self.Filename)>0:
                self.w = App()
                text, okPressed = QInputDialog.getText(self.w, "Rename", "Enetr New Name:", QLineEdit.Normal, "")
                if okPressed and text != '':
                    self.rename_message.append(text)
                    self.rename_message.append('rename')
                    self.rename_message.insert(0,self.connected_name)
                    self.rename_message.insert(1,self.sockName)
                    self.rename_message.insert(2,'\\'.join(self.path[1:]))
                    self.rename_message.insert(3,self.Filename[-1])
                    self.sock.send(pickle.dumps(self.rename_message))
    def Forward(self,MainWindow):
        if self.accessed_device == False and len(self.path)>0:
            self.lineEdit.setText('This PC\\'+self.lineEdit.text())
            if os.path.isdir(str(self.lineEdit.text()).replace('This PC\\','')):
                self.available_Folders.clear()
                self.available_Folders.append('...')
                self.listWidget.clear()
                self.path = self.lineEdit.text().split('\\')
                self.dir_list_folder(self.lineEdit.text().replace('This PC\\',''))
                self.change_item_listwidget(self.available_Folders)
            else:
                self.warning = App()
                buttonReply = QMessageBox.warning(self.warning, "warning",
                                                   "windows can't find '"+str(self.lineEdit.text())+"' check the spelling and try again",
                                                   QMessageBox.Ok, QMessageBox.Ok)
    def Backward(self):
        self.Filename =[]
        if self.accessed_device == False:
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
            self.lineEdit.setText(str(' \\ '.join(self.path)))
        if self.accessed_device == True:
            if len(self.path) > 1:
                print(self.path)
                del self.path[-1]
                self.request_message(self.path)
            elif len(self.path) == 1:
                self.path.clear()
                self.listWidget.clear()
                self.available_Folders = self.available_Device[:]
                self.change_item_listwidget(self.available_Folders)
                self.lineEdit.setText('')
    def Edit(self):
        os.startfile(shutil.which('Notepad'))

    def Copy(self):
        self.File_name_Cut = []
        if len(self.Filename)>0:
            if len(self.path) > 1 and self.Filename[-1] != '...'and self.accessed_device == False:
                self.File_name_Copy.append('\\'.join(self.path[1:]))
                self.File_name_Copy.append(self.Filename[-1])
                self.File_Copy = str('\\'.join(self.path[1:])) + '\\' + str(self.Filename[-1])
    def Cut(self):
        self.File_name_Copy = []
        if len(self.Filename)>0:
            if len(self.path) > 1 and self.Filename[-1] != '...':
                self.File_name_Cut.append('\\'.join(self.path[1:]))
                self.File_name_Cut.append(self.Filename[-1])
                self.File_Cut = str('\\'.join(self.path[1:])) + '\\' + str(self.Filename[-1])
    def Paste(self):
        if len(self.path) > 0:
            self.paste = '\\'.join(self.path[1:])
        if self.accessed_device == False:
            if len(self.File_name_Copy)!=0:
                if self.paste != self.File_name_Copy[0]:
                    try:
                        shutil.copytree(self.File_Copy, self.paste+'\\'+str(self.File_name_Copy[-1]))
                        self.available_Folders.append(self.File_name_Copy[-1])
                    except:
                        shutil.copy(self.File_Copy , self.paste+'\\'+str(self.File_name_Copy[-1]))
                        self.available_Folders.append(self.File_name_Copy[-1])
                else:
                    if self.file_or_folder(self.File_name_Copy[-1]) == 'Folder':
                        th = 1
                        while os.path.isdir(self.paste + '\\' + self.File_name_Copy[-1] + '(' + str(th) + ')') == True:
                            th += 1
                        try:
                            shutil.copytree(self.File_Copy, self.paste+'\\'+str(self.File_name_Copy[-1])+'('+str(th)+')')
                            self.available_Folders.append(self.File_name_Copy[-1]+'('+str(th)+')')
                        except:
                            pass
                    if self.file_or_folder(self.File_name_Copy[-1]) == 'File':
                        for format in self.Formats:
                            if self.File_name_Copy[-1].endswith(format):
                                try:
                                    th = 1
                                    self.File_name_Copy[-1] = self.File_name_Copy[-1].replace(format,'')
                                    shutil.copy(self.File_Copy , self.paste+'\\'+str(self.File_name_Copy[-1])+'('+str(th)+')'+format)
                                    self.available_Folders.append(self.File_name_Copy[-1]+'('+str(th)+')'+format)
                                    th += 1
                                except:
                                    pass
                self.listWidget.clear()
                self.change_item_listwidget(self.available_Folders)
                self.File_name_Copy.clear()
            if len(self.File_name_Cut)!=0:
                if self.File_name_Cut[-1] not in os.listdir(self.paste):
                    try:
                        shutil.copytree(self.File_Cut, self.paste+'\\'+str(self.File_name_Cut[-1]))
                        self.available_Folders.append(self.File_name_Cut[-1])
                    except:
                        shutil.copy(self.File_Cut , self.paste+'\\'+str(self.File_name_Cut[-1]))
                        self.available_Folders.append(self.File_name_Cut[-1])
                else:
                    pass
                try:
                    os.remove(str(self.File_Cut))
                except:
                    shutil.rmtree(str(self.File_Cut))

                self.listWidget.clear()
                self.change_item_listwidget(self.available_Folders)
                self.File_name_Cut.clear()
        if self.accessed_device == True:
            if len(self.path) > 1:
                self.cut_message.append(self.File_Cut)
                self.cut_message.append(self.paste+'\\'+str(self.File_name_Cut[-1]))
                self.cut_message.insert(0,self.path[0])
                if len(self.path[1:]) == 1:
                    self.cut_message.append(''.join(self.path[1:])+'\\')
                else:
                    self.cut_message.append('\\'.join(self.path[1:]))
                self.Cut_message(self.cut_message)
    def request_message(self,dir):
        dir.append('request')
        dir.insert(1,self.sockName)
        self.sock.send(pickle.dumps(dir))
        dir.remove('request')
        dir.remove(self.sockName)
    def Delete_message(self,list):
        list.append('Delete')
        list.insert(1, self.sockName)
        self.sock.send(pickle.dumps(list))
        list.remove('Delete')
        list.remove(self.sockName)
    def Delete_for_otherDevice(self,recieve):
        try:
            os.remove('\\'.join(recieve[2:-1]))
        except:
            shutil.rmtree('\\'.join(recieve[2:-1]))
        First = os.getcwd()
        os.chdir('C:\\')
        tobesend = os.listdir('\\'.join(recieve[2:-2]))
        tobesend.append('order')
        tobesend.insert(0, recieve[1])
        tobesend.insert(1, recieve[0])
        self.sock.send(pickle.dumps(tobesend))
        os.chdir(First)
    def send_directory(self,recieve):
        if len(recieve) == 3:
            tobesend = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
            tobesend.append('order')
            tobesend.insert(0, recieve[1])
            tobesend.insert(1, recieve[0])
            self.sock.send(pickle.dumps(tobesend))
            tobesend.clear()
        if len(recieve) > 3:
            First = os.getcwd()
            os.chdir('C:\\')
            tobesend = os.listdir('\\'.join(recieve[2:-1]))
            tobesend.append('order')
            tobesend.insert(0, recieve[1])
            tobesend.insert(1, recieve[0])
            self.sock.send(pickle.dumps(tobesend))
            os.chdir(First)
    def recieve_directory(self,recieve):
        self.listWidget.clear()
        self.available_Folders = recieve[2:-1]
        self.available_Folders.insert(0, '...')
        if '$RECYCLE.BIN' in self.available_Folders:
            self.available_Folders.remove('$RECYCLE.BIN')
        if 'System Volume Information' in self.available_Folders:
            self.available_Folders.remove('System Volume Information')
        self.change_item_listwidget(self.available_Folders)
        self.lineEdit.setText(' \\ '.join(self.path))
    def Cut_message(self,list):
        list.append('cut')
        list.insert(1,self.sockName)
        self.sock.send(pickle.dumps(list))
        list.clear()
    def cut_for_otherDevice(self,recieve):
        try:
            shutil.copytree(recieve[2], recieve[3])
        except:
            shutil.copy(recieve[2], recieve[3])
        try:
            os.remove(recieve[2])
        except:
            shutil.rmtree(recieve[2])
        tobesend = os.listdir(recieve[4])
        tobesend.append('order')
        tobesend.insert(0, recieve[1])
        tobesend.insert(1, recieve[0])
        self.sock.send(pickle.dumps(tobesend))
    def newFolder_Message(self,list):
        list.append('NewFolder')
        list.insert(1,self.sockName)
        self.sock.send(pickle.dumps(list))
        list.clear()
    def NewFolder_for_otherDevice(self,recieve):
        if os.path.isdir(recieve[-2] + '\\' + 'New Folder') == False:
            os.mkdir(recieve[-2] + '\\' + 'New Folder')
        else:
            th = 1
            while os.path.isdir(recieve[-2] + '\\' + 'New Folder' + '(' + str(th) + ')') == True:
                th += 1
            os.mkdir(recieve[-2] + '\\' + 'New Folder' + '(' + str(th) + ')')
        First = os.getcwd()
        os.chdir('C:\\')
        tobesend = os.listdir(recieve[2])
        tobesend.append('order')
        tobesend.insert(0, recieve[1])
        tobesend.insert(1, recieve[0])
        self.sock.send(pickle.dumps(tobesend))
        os.chdir(First)
    def Download(self):
        if self.accessed_device == True and len(self.path) > 1:
            if self.file_or_folder(self.Filename[-1]) == 'File':
                self.download_message(self.Filename[-1],self.path)
            elif self.file_or_folder(self.Filename[-1]) == 'Folder':
                self.download_Folder(self.Filename[-1],self.path)

    def download_Folder(self,name,path):
        try:
            os.makedirs(self.download_place +'\\'+ name)
        except:
            pass
        if len(os.listdir('\\'.join(path[1:])+'\\'+name))>0:
            for i in os.listdir('\\'.join(path[1:])+'\\'+name):
                if self.file_or_folder(i) == 'Folder':
                    name = name+'\\'+i
                    self.download_Folder(name,path)
                    name = name.replace('\\'+i,'')
                else:
                    name = name + '\\' + i
                    self.download_message(name,path)
                    name = name.replace('\\' + i, '')

    def download_message(self,name,path):
        self.Download_Message = []
        self.Download_Message.append('\\'.join(path[1:])+'\\'+name)
        self.Download_Message.append('Download_Message')
        self.Download_Message.insert(0,self.path[0])
        self.Download_Message.insert(1,self.sockName)
        self.file = open(self.download_place+'\\'+name,'wb')
        self.sock.send(pickle.dumps(self.Download_Message))

    def send(self):
        if self.accessed_device == False and len(self.Filename)>0 and self.file_or_folder(self.Filename[-1])=='File':
            self.send_message = []
            self.send_message.append(self.Filename[-1])
            self.send_message.append('send')
            self.send_message.insert(0,self.connected_name)
            self.send_message.insert(1,self.sockName)
            self.sock.send(pickle.dumps(self.send_message))
            file = open('\\'.join(self.path[1:])+'\\'+self.Filename[-1], 'rb')
            read = file.read(10000000)
            while read:
                print(read)
                self.sock.send(read)
                read = file.read(10000000)
                if not read:
                    break
            file.close()
    def chat(self):
        if self.lineEdit2.text()!= '':
            itm = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setFamily("Sitka Text")
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            itm.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.NoBrush)
            itm.setForeground(brush)
            itm.setText(self.sockName+' :: '+self.lineEdit2.text())
            self.chatroom.addItem(itm)
            self.sock.send(pickle.dumps([self.connected_name,self.sockName,self.lineEdit2.text(),'chat']))
            self.lineEdit2.clear()
    def reply_Download(self,recieve):
        file = open(recieve[-2], 'rb')
        read = file.read(10000000)
        while read:
            self.sock.send(read)
            read = file.read(10000000)
            if not read:
                break
        file.close()
    def Thread_chat(self,recieve):
        itm = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        itm.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        itm.setForeground(brush)
        itm.setText(recieve[-3] + ' :: ' + recieve[-2])
        self.chatroom.addItem(itm)
    def reply_rename(self,recieve):
        os.rename(recieve[2] + '\\' + recieve[3], recieve[2] + '\\' + recieve[-2])
        First = os.getcwd()
        os.chdir('C:\\')
        tobesend = os.listdir(recieve[2])
        tobesend.append('order')
        tobesend.insert(0, recieve[1])
        tobesend.insert(1, recieve[0])
        self.sock.send(pickle.dumps(tobesend))
        os.chdir(First)
