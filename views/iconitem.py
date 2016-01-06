#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class IconItem(QFrame):
    style = '''
        QFrame#IconItem{
            background-color: gray;
            border: 1px solid black;
        }
    '''

    selfRemoved = pyqtSignal(unicode)

    def __init__(self, key=None, parent=None):
        super(IconItem, self).__init__(parent)
        self.setObjectName("IconItem")
        self._key = key
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        pass

    def initUI(self):
        self.iconLabel = QLabel(self)
        self.textLabel = QLabel(self)
        self.textLabel.setAlignment(Qt.AlignCenter)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.iconLabel)
        mainLayout.addWidget(self.textLabel)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        self.setStyleSheet(self.style)

    def initConnect(self):
        pass

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QPixmap(icon))

    def setText(self, text):
        self.textLabel.setText(text)

    def setKey(self, key):
        self._key = key

    def mouseDoubleClickEvent(self, event):
        self.selfRemoved.emit(self._key)
        super(IconItem, self).mouseDoubleClickEvent(event)
