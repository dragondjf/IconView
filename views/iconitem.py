#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class IconItem(QFrame):
    """docstring for IconItem"""
    def __init__(self, parent=None):
        super(IconItem, self).__init__(parent)
    
    def initData(self):
        pass

    def initUI(self):
        self.iconLable = QLabel(self)
        self.textLable = QLabel(self)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.iconLable)
        mainLayout.addWidget(self.textLable)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

    def initConnect(self):
        pass

    def setIcon(self, icon):
        self.iconLable.setPixmap(QPixmap(icon))

    def setText(self, text):
        self.textLabel.setText(text)
