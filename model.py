import sys
from PyQt5.QtCore import QSortFilterProxyModel,QFile,QTextStream,QDir,QStringListModel ,QDirIterator,QFileInfo,QModelIndex,Qt
from PyQt5.QtWidgets import QFileIconProvider 

iconProvider = QFileIconProvider()# siglton

class SimpleFileSystemModel(QStringListModel ):

    def __init__(self,parent,path):
        QStringListModel .__init__(self,parent)
        
        self.setRootPath(path)
    
    
    def setRootPath(self,path):
        lst=[]
        it = QDirIterator(path,QDir.AllDirs|QDir.Files|QDir.NoDotAndDotDot,QDirIterator.NoIteratorFlags)
        while it.hasNext():
             lst.append(it.next())
        self.setStringList(lst)        

    def fileInfo(self, index):
        inf=QFileInfo(QStringListModel.data(self, index, Qt.DisplayRole))
        return inf
        
    def data(self, index, role):
        
        if role==Qt.DisplayRole:
            return self.fileInfo(index).fileName()
        elif role==Qt.DecorationRole:
            return iconProvider.icon(self.fileInfo(index))
        return QStringListModel.data(self, index, role)



class FilterdFileSystemModel(QSortFilterProxyModel):
    def __init__(self,parent,path):
        QSortFilterProxyModel.__init__(self,parent)
        self.file_model =  SimpleFileSystemModel(self,path)
        self.setSourceModel(self.file_model)
        self.sort(0);

    
    def lessThan(self,left,right):
        inf1=self.file_model.fileInfo(left)
        inf2=self.file_model.fileInfo(right)

        if inf1.isFile() and not inf2.isFile():
            return False
        if not inf1.isFile() and inf2.isFile():
            return True
        
        return inf1.fileName().isupper()<inf2.fileName().isupper()
        


    def setRootPath(self,path):
        self.file_model.setRootPath(path)
        
    def toCSV(self,filename):
        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            print('file open error')
            return
        stream = QTextStream(file)
        lst=self.file_model.stringList()
        for row in range(self.rowCount()):
            index = self.mapToSource(self.index(row, 0))
            stream <<lst[index.row()]<<';\n'
        file.close();
            
        
        
                    
        
        

   
