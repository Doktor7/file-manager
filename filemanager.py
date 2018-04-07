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
        if self.accessed_device == False and len(self.Filename)>0:
            self.send_message = []
            self.send_message.append(self.Filename[-1])
            self.send_message.append('send')
            self.send_message.insert(0,self.connected_name)
            self.send_message.insert(1,self.sockName)
            self.sock.send(pickle.dumps(self.send_message))
            file = open('\\'.join(self.path[1:])+'\\'+self.Filename[-1], 'rb')
            read = file.read()
            while True:
                self.sock.send(read)
                read = file.read()
                if not read:
                    break
            file.close()
    def chat(self):
        if self.lineEdit2.text()!= '':
            itm = QtWidgets.QListWidgetItem()
            itm.setText(self.sockName+' :: '+self.lineEdit2.text())
            self.chatroom.addItem(itm)
            self.sock.send(pickle.dumps([self.connected_name,self.sockName,self.lineEdit2.text(),'chat']))
            self.lineEdit2.clear()
