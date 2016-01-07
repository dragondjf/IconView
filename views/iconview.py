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

    heightChanged = pyqtSignal(int)

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
        self.heightChanged.emit(availableHeight)
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


    def __init__(self, isVerticalBarAlwaysOff=False, parent=None):
        super(IconView, self).__init__(parent)
        self._isVerticalBarAlwaysOff = isVerticalBarAlwaysOff
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        if self._isVerticalBarAlwaysOff:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.initData()
        self.initUI()
        self.initConnect()

        self.setGridParameters(100, 50, 30, 30, 30, 30, 30, 0)

    def initData(self):
        pass

    def initUI(self):
        self.setMinimumSize(400, 400)
        # self.resize(800, 600)
        self.centerWidget = IconViewCenterWidget(self)
        self.initItemManager()
        self.setItems(self.itemManager.items())

        self.setWidget(self.centerWidget)
        

    def initConnect(self):
        # self.requestChangeGridParameters.connect(self.setGridParameters)
        # self.requestChangeXFixedSpacing.connect(self.setXFixedSpacing)
        # self.requestChangeYFixedSpacing.connect(self.setYFixedSpacing)
        # self.requestChangeGridWidth.connect(self.setGridWidth)
        # self.requestChangeGridHeight.connect(self.setGridHeight)
        # self.requestChangeLeftMargin.connect(self.setLeftMargin)
        # self.requestChangeTopMargin.connect(self.setTopMargin)
        # self.requestChangeRightMargin.connect(self.setRightMargin)
        # self.requestChangeBottomMargin.connect(self.setBottomMargin)
        # self.requestChangeMargins.connect(self.setMargins)

        self.itemManager.itemsChanged.connect(self.reLayoutItems)

    def initItemManager(self):
        self.itemManager = ItemManager(self.centerWidget)

    def setItems(self, items):
        self.centerWidget.setItems(items)
        if self._isVerticalBarAlwaysOff:
            availableHeight = self.centerWidget.gridManager().getHeightByFixWidth(self.width(), len(self.items()))
            self.setFixedHeight(availableHeight)
        else:
            pass

    def items(self):
        return self.centerWidget.items()

    def setGridParameters(self, gridWidth, gridHeight, xFixedSpacing, yFixedSpacing, leftMargin, topMargin, rightMargin, bottomMargin):
        self.centerWidget.gridManager().setGridWidth(gridWidth)
        self.centerWidget.gridManager().setGridHeight(gridHeight)
        self.centerWidget.gridManager().setXFixedSpacing(xFixedSpacing)
        self.centerWidget.gridManager().setYFixedSpacing(yFixedSpacing)
        self.setMargins(leftMargin, topMargin, rightMargin, bottomMargin)

    def setMargins(self, leftMargin, topMargin, rightMargin, bottomMargin):
        self.centerWidget.gridManager().setLeftMargin(leftMargin)
        self.centerWidget.gridManager().setTopMargin(topMargin)
        self.centerWidget.gridManager().setRightMargin(rightMargin)
        self.centerWidget.gridManager().setBottomMargin(bottomMargin)
        self.centerWidget.reLayoutItems()

    def setGridWidth(self, gridWidth):
        self.centerWidget.gridManager().setGridWidth(gridWidth)
        self.centerWidget.reLayoutItems()

    def setGridHeight(self, gridHeight):
        self.centerWidget.gridManager().setGridHeight(gridHeight)
        self.centerWidget.reLayoutItems()
    
    def setXFixedSpacing(self, xFixedSpacing):
        self.centerWidget.gridManager().setXFixedSpacing(xFixedSpacing)
        self.centerWidget.reLayoutItems()

    def setYFixedSpacing(self, yFixedSpacing):
        self.centerWidget.gridManager().setYFixedSpacing(yFixedSpacing)
        self.centerWidget.reLayoutItems()

    def setLeftMargin(self, leftMargin):
        self.centerWidget.gridManager().setLeftMargin(leftMargin)
        self.centerWidget.reLayoutItems()

    def setTopMargin(self, topMargin):
        self.centerWidget.gridManager().setTopMargin(topMargin)
        self.centerWidget.reLayoutItems()

    def setRightMargin(self, rightMargin):
        self.centerWidget.gridManager().setRightMargin(rightMargin)
        self.centerWidget.reLayoutItems()

    def setBottomMargin(self, bottomMargin):
        self.centerWidget.gridManager().setBottomMargin(bottomMargin)
        self.centerWidget.reLayoutItems()

    def resizeEvent(self, event):
        self.centerWidget.updateSize(event.size().width())
        super(IconView, self).resizeEvent(event)

    def reLayoutItems(self, items):
        self.centerWidget.setItems(items)
        self.centerWidget.updateHeightByWidth(self.width())
