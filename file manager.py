from PyQt5 import QtCore, QtGui, QtWidgets
import os , string

class Ui_MainWindow(object):
    def __init__(self):
        self.available_Folders = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        self.available_Drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        self.available_Drives2 = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    def set_icon(self,file,icon):
        self.Formats = ['pdf','mp3','jpg','aac','avi','bmp','chm','css','defult','dll','doc','docx',\
                        'fla','htm','html','ini','jar','jpeg','js','lasso','mdp','mov','mp4','mpg',\
                        'ogg','ogv','php','png','ppt','py','rb','real','reg','rtf','sgl','swf','txt',\
                        'vbs','wav','webm','wmv','xls','xlsx','xml','xsl','zip','rar','mkv','exe','srt','3gp',\
                        'log']
        for format in self.Formats:
            if self.available_Folders[file].endswith(format):
                icon.addPixmap(QtGui.QPixmap(format), QtGui.QIcon.Normal, QtGui.QIcon.On)
    def change_item_listwidget(self,list):
        for i in range(len(self.available_Folders)):
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            if str(self.available_Folders[i]).find(':') != -1:
                icon.addPixmap(QtGui.QPixmap('drive icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            else:
                icon.addPixmap(QtGui.QPixmap('_Close.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.set_icon(i,icon)
            item.setIcon(icon)
            item.setText(str(self.available_Folders[i]))
            self.listWidget.addItem(item)
    def setupUi(self, MainWindow):
        self.address_bar = ''
        self.path = []
        self.opening_lst = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 600, 600))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.change_item_listwidget(self.available_Folders)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.listWidget.itemDoubleClicked.connect(self.selecticoncange)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #print(self.path)

    def file_or_folder(self, text):
        flag = False
        for each_format in self.Formats:
            if text.endswith(each_format) == True:
                flag = True
        if flag == True:
            return 'File'
        else:
            return 'Folder'
    def dir_list_folder(self,paths):
         for folderName in os.listdir(paths):
             if folderName != '$RECYCLE.BIN' and folderName != 'System Volume Information':
                self.available_Folders.append(folderName)

    def selecticoncange(self):
        self.available_Folders.clear()
        self.available_Folders.append('...')
        for currentitem in self.listWidget.selectedItems():
            self.opening_lst.append(currentitem.text())
            self.path.append(currentitem.text())
            # print(self.path)
            if currentitem.text() == '...' and len(self.path) != 2:
                del self.path[-1]
                del self.path[-1]
            if currentitem.text() == '...' and len(self.path) == 2:
                # print('kir')
                self.listWidget.clear()
                self.path.clear()
                self.available_Folders = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

            if len(self.path) == 1:
                self.dir_list_folder(self.path[0] + '/')
            if len(self.path) > 1:
                if self.file_or_folder(currentitem.text()) == 'Folder':
                    self.dir_list_folder('/'.join(self.path))
                if self.file_or_folder(currentitem.text()) == 'File':
                    os.startfile('/'.join(self.path))
        # print(self.path)
        if len(self.path) > 0:
            if self.file_or_folder(self.path[-1]) == 'Folder':
                self.listWidget.clear()
                self.lineEdit.setText(str('/'.join(self.path)))
            if self.file_or_folder(self.path[-1]) == 'File':
                del self.path[-1]
                del self.available_Folders[-1]
        if len(self.path) == 0:
            self.lineEdit.setText('')

        # print(self.path)
        # print(self.available_Folders)
        self.change_item_listwidget(self.available_Folders)
        # print(self.available_Folders)

while True:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
