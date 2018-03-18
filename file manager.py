from PyQt5 import QtCore, QtGui, QtWidgets
import os, string, shutil


class Ui_MainWindow(object):
    def __init__(self):
        self.available_Folders = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        self.available_Drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        self.available_Drives2 = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

    def set_icon(self, file, icon):
        self.Formats = ['pdf', 'mp3', 'jpg', 'aac', 'avi', 'bmp', 'chm', 'css', 'defult', 'dll', 'doc', 'docx', \
                        'fla', 'htm', 'html', 'ini', 'jar', 'jpeg', 'js', 'lasso', 'mdp', 'mov', 'mp4', 'mpg', \
                        'ogg', 'ogv', 'php', 'png', 'ppt', 'py', 'rb', 'real', 'reg', 'rtf', 'sgl', 'swf', 'txt', \
                        'vbs', 'wav', 'webm', 'wmv', 'xls', 'xlsx', 'xml', 'xsl', 'zip', 'rar', 'mkv', 'exe', 'srt',
                        '3gp','log', 'ico']
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
        self.listWidget.itemClicked.connect(self.selected)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 615, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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
        self.actionEdit_2 = QtWidgets.QAction(MainWindow)
        self.actionEdit_2.setIcon(icon)
        self.actionEdit_2.setObjectName("actionEdit_2")
        self.actionPaste_2 = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste_2.setIcon(icon5)
        self.actionPaste_2.setObjectName("actionPaste_2")
        self.actionFavorits = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Favorites.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFavorits.setIcon(icon6)
        self.actionFavorits.setObjectName("actionFavorits")
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
        self.toolBar.addAction(self.actionFavorits)
        self.toolBar.addAction(self.actionCopy_2)
        self.toolBar.addAction(self.actionForward)
        self.toolBar.addAction(self.actionBackward)
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
        self.actionFavorits.setText(_translate("MainWindow", "Favorits"))
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
        self.actionBackward.triggered.connect(self.Backward)
        self.actionNew_Folder.triggered.connect(self.add_New_Folder)
        self.actionDelete.triggered.connect(self.delete)
        self.actionDelete_2.triggered.connect(self.delete)
        self.actionExit_2.triggered.connect(self.close)
        self.actionRename_2.triggered.connect(self.rename)

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
        print(self.Filename)
        self.destiny = '/'.join(self.path)

        if self.Filename[-1] != '...' and len(self.Filename) != 0:
            try:
                os.remove(self.destiny + '/' + self.Filename[-1])
            except:
                shutil.rmtree(self.destiny + '/' + self.Filename[-1])
        if len(self.Filename) != 0:
            self.available_Folders.remove(str(self.Filename[-1]))
            self.listWidget.clear()
            self.change_item_listwidget(self.available_Folders)
            self.Filename.remove(self.Filename[0])

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

    def add_New_Folder(self):
        First_Directory = os.getcwd()
        current_address = '/'.join(self.path)
        if len(current_address) != 0:
            os.chdir(current_address)
        if os.path.isdir(current_address + '/' + 'New Folder') == False:
            os.mkdir('New Folder')

            os.chdir(First_Directory)
            self.available_Folders.append('New Folder')
        else:
            th = 1
            while os.path.isdir(current_address + '/' + 'New Folder' + '(' + str(th) + ')') == True:
                th += 1
            os.mkdir('New Folder' + '(' + str(th) + ')')
            os.chdir(First_Directory)
            self.available_Folders.append('New Folder' + '(' + str(th) + ')')
        self.listWidget.clear()
        self.change_item_listwidget(self.available_Folders)
        # print(First_Directory)
        # print(self.available_Folders)
        # print(self.available_Folders)

    def close(self):
        sys.exit(app.exec_())

    def rename(self):
        

        import tkinter as tk
        from tkinter import simpledialog
        window = tk.Tk()
        answer = simpledialog.askstring('rename', 'Enter New Name:', parent=window)
        First = os.getcwd()

        current = '/'.join(self.path)
        if len(current) != 0:
            os.chdir(current)
        if answer is not None:
            os.rename(self.Filename[-1], answer)
        os.chdir(First)
        self.available_Folders.remove(str(self.Filename[-1]))
        self.available_Folders.append(answer)
        self.listWidget.clear()
        self.change_item_listwidget(self.available_Folders)

    def Backward(self):

        if len(self.path) > 1:
            self.available_Folders.clear()
            self.listWidget.clear()
            self.available_Folders.append('...')
            del self.path[-1]
            self.dir_list_folder('/'.join(self.path))
            self.change_item_listwidget(self.available_Folders)
        if len(self.path) == 1:
            self.listWidget.clear()
            self.path.clear()
            self.available_Folders = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
            self.change_item_listwidget(self.available_Folders)


while True:
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
