#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .gridmanager import FixedSpacingGridManager
from .itemmanager import ItemManager


class IconViewCenterWidget(QFrame):
    
    style = '''
        QFrame{background-color: green};
    '''

    def __init__(self, parent=None):
        super(IconViewCenterWidget, self).__init__(None)
        self.parent = parent
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        self._gridManager = FixedSpacingGridManager()
        self._Items = []

    def initUI(self):
        self._gridManager.setGridParameters(100, 100, 10, 10, 10, 10, 10, 0)
        # self.setStyleSheet(self.style)
        pass

    def initConnect(self):
        pass

    def gridManager(self):
        return self._gridManager

    def items(self):
        return self._Items

    def setItems(self, items):
        self._Items = items

    def setGridParameters(self, gridWidth, gridHeight, xFixedSpacing, yFixedSpacing, leftMargin, topMargin, rightMargin, bottomMargin):
        self._gridManager.setGridParameters(gridWidth, gridHeight, xFixedSpacing, yFixedSpacing, leftMargin, topMargin, rightMargin, bottomMargin)

    def setMargins(self, leftMargin, topMargin, rightMargin, bottomMargin):
        self._gridManager.setMargins(leftMargin, topMargin, rightMargin, bottomMargin)

    def setGridWidth(self, gridWidth):
        self._gridManager.setGridWidth(gridWidth)

    def setGridHeight(self, gridHeight):
        self._gridManager.setGridHeight(gridHeight)

    def setXFixedSpacing(self, xFixedSpacing):
        self._gridManager.setXFixedSpacing(xFixedSpacing)

    def setYFixedSpacing(self, yFixedSpacing):
        self._gridManager.setYFixedSpacing(yFixedSpacing)

    def setLeftMargin(self, leftMargin):
        self._gridManager.setLeftMargin(leftMargin)

    def setTopMargin(self, topMargin):
        self._gridManager.setTopMargin(topMargin)

    def setRightMargin(self, rightMargin):
        self._gridManager.setRightMargin(rightMargin)

    def setBottomMargin(self, bottomMargin):
        self._gridManager.setBottomMargin(bottomMargin)

    def updateSize(self, width):
        if (self._gridManager.getAvaliableColumnCount(width) == self._gridManager.availableCount()):
            return
        self.updateHeightByWidth(width)

    def updateHeightByWidth(self, width):
        availableHeight = self._gridManager.getHeightByFixWidth(width, len(self.items()))
        self.setFixedSize(width, availableHeight)
        rect = QRect(0, 0, width , availableHeight)
        self.reLayoutItemsByRect(rect)

    def reLayoutItemsByRect(self, rect):
        self._gridManager.setGeometry(rect)
        self.reLayoutItems()

    def reLayoutItems(self):
        self._gridManager.generateGrids()
        items = self._gridManager.getListItems()
        for item in self.items():
            index = self.items().index(item)
            if index < len(items):
                gridItem =items[index]
                item.move(gridItem.pos())
                item.setFixedSize(gridItem.size())

    def paintEvent(self, event):
        if False:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            for gridItem in self._gridManager.getListItems():
                color = QColor(100, 100, 100, 255)
                painter.fillRect(gridItem.geometry(), color)
        super(IconViewCenterWidget, self).paintEvent(event)


class IconView(QScrollArea):

    requestChangeGridParameters = pyqtSignal(int, int, int, int, int, int, int, int)
    requestChangeGridWidth = pyqtSignal(int)
    requestChangeGridHeight = pyqtSignal(int)
    requestChangeXFixedSpacing = pyqtSignal(int)
    requestChangeYFixedSpacing = pyqtSignal(int)
    requestChangeLeftMargin= pyqtSignal(int)
    requestChangeTopMargin = pyqtSignal(int)
    requestChangeRightMargin = pyqtSignal(int)
    requestChangeBottomMargin = pyqtSignal(int)
    requestChangeMargins = pyqtSignal(int, int, int, int)


    def __init__(self, parent=None):
        super(IconView, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.initData()
        self.initUI()
        self.initConnect()

        self.requestChangeXFixedSpacing.emit(40)
        self.requestChangeGridParameters.emit(50, 50, 30, 30, 30, 30, 30, 0)

    def initData(self):
        pass

    def initUI(self):
        self.centerWidget = IconViewCenterWidget(self)
        self.initItemManager()
        self.centerWidget.setItems(self.itemManager.items())

        self.setWidget(self.centerWidget)
        self.setMinimumSize(400, 400)
        self.resize(800, 600)

    def initConnect(self):
        self.requestChangeGridParameters.connect(self.updateViewByGridParameters)
        self.requestChangeXFixedSpacing.connect(self.updateViewByXFixedSpacing)
        self.requestChangeYFixedSpacing.connect(self.updateViewByYFixedSpacing)
        self.requestChangeGridWidth.connect(self.updateViewByGridWidth)
        self.requestChangeGridHeight.connect(self.updateViewByGridHeight)
        self.requestChangeLeftMargin.connect(self.updateViewByLeftMargin)
        self.requestChangeTopMargin.connect(self.updateViewByTopMargin)
        self.requestChangeRightMargin.connect(self.updateViewByRightMargin)
        self.requestChangeBottomMargin.connect(self.updateViewByBottomMargin)
        self.requestChangeMargins.connect(self.updateViewByMargins)

        self.itemManager.itemsChanged.connect(self.reLayoutItems)

    def initItemManager(self):
        self.itemManager = ItemManager(self.centerWidget)

    def updateViewByGridParameters(self, gridWidth, gridHeight, xFixedSpacing, yFixedSpacing, leftMargin, topMargin, rightMargin, bottomMargin):
        self.centerWidget.gridManager().setGridWidth(gridWidth)
        self.centerWidget.gridManager().setGridHeight(gridHeight)
        self.centerWidget.gridManager().setXFixedSpacing(xFixedSpacing)
        self.centerWidget.gridManager().setYFixedSpacing(yFixedSpacing)
        self.updateViewByMargins(leftMargin, topMargin, rightMargin, bottomMargin)

    def updateViewByMargins(self, leftMargin, topMargin, rightMargin, bottomMargin):
        self.centerWidget.gridManager().setLeftMargin(leftMargin)
        self.centerWidget.gridManager().setTopMargin(topMargin)
        self.centerWidget.gridManager().setRightMargin(rightMargin)
        self.centerWidget.gridManager().setBottomMargin(bottomMargin)
        self.centerWidget.reLayoutItems()

    def updateViewByGridWidth(self, gridWidth):
        self.centerWidget.gridManager().setGridWidth(gridWidth)
        self.centerWidget.reLayoutItems()

    def updateViewByGridHeight(self, gridHeight):
        self.centerWidget.gridManager().setGridHeight(gridHeight)
        self.centerWidget.reLayoutItems()
    
    def updateViewByXFixedSpacing(self, xFixedSpacing):
        self.centerWidget.gridManager().setXFixedSpacing(xFixedSpacing)
        self.centerWidget.reLayoutItems()

    def updateViewByYFixedSpacing(self, yFixedSpacing):
        self.centerWidget.gridManager().setYFixedSpacing(yFixedSpacing)
        self.centerWidget.reLayoutItems()

    def updateViewByLeftMargin(self, leftMargin):
        self.centerWidget.gridManager().setLeftMargin(leftMargin)
        self.centerWidget.reLayoutItems()

    def updateViewByTopMargin(self, topMargin):
        self.centerWidget.gridManager().setTopMargin(topMargin)
        self.centerWidget.reLayoutItems()

    def updateViewByRightMargin(self, rightMargin):
        self.centerWidget.gridManager().setRightMargin(rightMargin)
        self.centerWidget.reLayoutItems()

    def updateViewByBottomMargin(self, bottomMargin):
        self.centerWidget.gridManager().setBottomMargin(bottomMargin)
        self.centerWidget.reLayoutItems()

    def resizeEvent(self, event):
        self.centerWidget.updateSize(event.size().width())
        super(IconView, self).resizeEvent(event)

    def reLayoutItems(self, items):
        self.centerWidget.setItems(items)
        self.centerWidget.updateHeightByWidth(self.width())
