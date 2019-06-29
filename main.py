import sys
import os


from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListView,QWidget,QVBoxLayout,QLineEdit,QPushButton,QFileDialog
from PyQt5.QtCore  import QRegExp
from model import FilterdFileSystemModel
from widgets import FilterLine



class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.home_dir_path=os.getenv('HOME')
        self.setWindowTitle("Example")
        self.proxyModel   = FilterdFileSystemModel(self,self.home_dir_path)
        
        self.line   = FilterLine()
        self.lst    = QListView()
        self.lst.setModel(self.proxyModel)
        self.sel_dir=QPushButton(self.home_dir_path)
        self.sel_dir.clicked.connect(self.selectRootPath)

        to_csv=QPushButton('Export to CSV')
        to_csv.clicked.connect(self.sendToCSV)
      
        layout = QVBoxLayout()
        layout.addWidget(self.sel_dir)
        layout.addWidget(self.line)
        layout.addWidget(self.lst)
        layout.addWidget(to_csv)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.resize(200, 480)
        self.line.filterChanged.connect(self.textFilterChanged)


    def textFilterChanged(self):
        regExp =QRegExp(self.line.text(),0,self.line.patternSyntax())
        self.proxyModel.setFilterRegExp(regExp)
        

    def sendToCSV(self):
        path = QFileDialog.getSaveFileName(self, 'To CSV', '', 'CSV(*.csv)')
        if path[0]:
             self.proxyModel.toCSV(path[0])

    def selectRootPath(self):
        d = QFileDialog.getExistingDirectory(self,'Select Directory', self.home_dir_path,QFileDialog.ShowDirsOnly)
        if d:
            self.home_dir_path=d
            self.proxyModel.setRootPath(d)
            self.sel_dir.setText(d)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Widget()
    window.show()
    sys.exit(app.exec_())
