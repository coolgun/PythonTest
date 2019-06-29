import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import *



class    FilterLine(QLineEdit):

    filterChanged = QtCore.pyqtSignal()

    def __init__(self,path='',parent=None):
        super().__init__(parent)

        self.m_patternGroup =QActionGroup(self)
    
        self.setClearButtonEnabled(True)
        self.textChanged.connect(self.filterChanged)
        menu = QMenu(self)
        self.m_patternGroup.setExclusive(True)

        patternAction = menu.addAction('Fixed String')
        patternAction.setData(QtCore.QRegExp.FixedString)
        patternAction.setCheckable(True)
        patternAction.setChecked(True)

        self.m_patternGroup.addAction(patternAction)
        patternAction = menu.addAction('Regular Expression')
        patternAction.setCheckable(True)
        patternAction.setData(QtCore.QRegExp.RegExp2)
        self.m_patternGroup.addAction(patternAction)

        patternAction = menu.addAction('Wildcard')
        patternAction.setCheckable(True)
        patternAction.setData(QtCore.QRegExp.Wildcard)
        self.m_patternGroup.addAction(patternAction)

        self.m_patternGroup.triggered.connect(self.filterChanged)

        optionsButton = QToolButton()
        optionsButton.setFocusPolicy(QtCore.Qt.NoFocus)
        optionsButton.setStyleSheet('* { border: none }')
        optionsButton.setMenu(menu)
        optionsButton.setPopupMode(QToolButton.InstantPopup)

        optionsAction = QWidgetAction(self)
        optionsAction.setDefaultWidget(optionsButton)
        self.addAction(optionsAction, QLineEdit.LeadingPosition)

    def patternSyntax(self):
        return self.m_patternGroup.checkedAction().data()
