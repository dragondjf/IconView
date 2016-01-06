#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GridItem(QObject):
    """docstring for GridItem"""
    def __init__(self, row, column, geometry, parent=None):
        super(GridItem, self).__init__(parent)
        self._row =  row
        self._column = column
        self._pos = QPoint(0, 0)
        self._geometry = geometry

    def row(self):
        return self._row

    def setRow(self, row):
        self._row = row

    def column(self):
        return self._column
    
    def setColumn(self, column):
        self._column = column

    def pos(self):
        return QPoint(self._geometry.x(), self._geometry.y())

    def size(self):
        return QSize(self._geometry.width(), self._geometry.height())

    def geometry(self):
        return self._geometry

    def setGeometry(self, rect):
        self._geometry = rect

    def key(self):
        return "%s-%s" % (self._geometry.x(), self._geometry.y())
