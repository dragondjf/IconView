#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SignalManager(QObject):

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)


signalManger = SignalManager()



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


class GridManager(QObject):
    geometryChanged = pyqtSignal(QRect)
    gridWidthChanged = pyqtSignal(int)
    gridHeightChanged = pyqtSignal(int)
    xMinimumSpacingChanged = pyqtSignal(int)
    yMinimumSpacingChanged = pyqtSignal(int)
    xFixedSpacingChanged = pyqtSignal(int)
    yFixedSpacingChanged = pyqtSignal(int)
    leftMarginChanged = pyqtSignal(int)
    topMarginChanged = pyqtSignal(int)
    rightMarginChanged = pyqtSignal(int)
    bottomMarginChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GridManager, self).__init__(parent)
        self._geometry = QRect(0, 0, 0, 0)
        self._availableWidth = 0
        self._availableHeight = 0
        self._availableX = 0
        self._availableY = 0
        self._availableRect = QRect(0, 0, 0, 0)
        self._gridWidth =  0
        self._gridHeight = 0
        self._xMinimumSpacing = 0
        self._yMinimumSpacing = 0
        self._xFixedSpacing = 0
        self._yFixedSpacing = 0
        self._leftMargin = 0
        self._rightMargin = 0
        self._topMargin = 0
        self._bottomMargin = 0

        self._rowCount = 0
        self._columnCount = 0
        self._xSpacing = 0
        self._ySpacing = 0

        self._list_items = []
        self._map_items = {}

    def geometry(self):
        return self._geometry

    def setGeometry(self, geometry):
        self._geometry = geometry
        self.geometryChanged.emit(geometry)

    def gridWidth(self):
        return self._gridWidth

    def setGridWidth(self, gridWidth):
        self._gridWidth = gridWidth
        self.gridWidthChanged.emit(gridWidth)

    def gridHeight(self):
        return self._gridHeight

    def setGridHeight(self, height):
        self._gridHeight = height
        self.gridHeightChanged.emit(height)

    def xMinimumSpacing(self):
        return self._xMinimumSpacing

    def setXMinimumSpacing(self, xMinimumSpacing):
        self._xMinimumSpacing = xMinimumSpacing
        self.xMinimumSpacingChanged.emit(xMinimumSpacing)

    def yMinimumSpacing(self):
        return self._yMinimumSpacing

    def setYMinimumSpacing(self, yMinimumSpacing):
        self._yMinimumSpacing = yMinimumSpacing
        self.yMinimumSpacingChanged.emit(yMinimumSpacing)

    def xFixedSpacing(self):
        return self._xFixedSpacing

    def setXFixedSpacing(self, xFixedSpacing):
        self._xFixedSpacing = xFixedSpacing
        self.xFixedSpacingChanged.emit(xFixedSpacing)

    def yFixedSpacing(self):
        return self._yFixedSpacing

    def setYFixedSpacing(self, yFixedSpacing):
        self._yFixedSpacing = yFixedSpacing
        self.yFixedSpacingChanged.emit(yFixedSpacing)

    def leftMargin(self):
        return self._leftMargin

    def setLeftMargin(self, leftMargin):
        self._leftMargin = leftMargin
        self.leftMarginChanged.emit(leftMargin)

    def topMargin(self):
        return self._topMargin

    def setTopMargin(self, topMargin):
        self._topMargin = topMargin
        self.topMarginChanged.emit(topMargin)

    def rightMargin(self):
        return self._rightMargin

    def setRightMargin(self, rightMargin):
        self._rightMargin = rightMargin
        self.rightMarginChanged.emit(rightMargin)

    def bottomMargin(self):
        return self._bottomMargin

    def setBottomMargin(self, bottomMargin):
        self._bottomMargin = bottomMargin
        self.bottomMarginChanged.emit(bottomMargin)

    def rowCount(self):
        return self._rowCount

    def columnCount(self):
        return self._columnCount

    def getItemByPos(self, pos):
        key = "%d-%d" % (pos.x(), pos.y())
        if key in self._map_items:
            return self._map_items[key]
        return None

    def getListItems(self):
        return self._list_items

    def getMapItems(self):
        return self._map_items


class DynamicSpacingGridManager(GridManager):
    """docstring for DynamicSpacingGridManager"""
    def __init__(self):
        super(DynamicSpacingGridManager, self).__init__()

    def initGridParameter(self, gridWidth, gridHeight, xMinimumSpacing, yMinimumSpacing, leftMargin, topMargin, rightMargin, bottomMargin):
        self._gridWidth = gridWidth
        self._gridHeight = gridHeight
        self._xMinimumSpacing = xMinimumSpacing
        self._yMinimumSpacing = yMinimumSpacing
        self._leftMargin = leftMargin
        self._topMargin = topMargin
        self._rightMargin = rightMargin
        self._bottomMargin = bottomMargin

    def generateGridsByRect(self, geometry):
        self._list_items = []
        self._map_items = {}
        self._geometry = geometry

        self._availableWidth = geometry.width() - self._leftMargin - self._rightMargin
        self._availableHeight = geometry.height() - self._topMargin - self._bottomMargin
        self._availableX = self._geometry.x() + self._leftMargin
        self._availableY = self._geometry.y() + self._topMargin
        self._availableRect = QRect(self._availableX, self._availableY, self._availableWidth, self._availableHeight)

        self._columnCount = self._availableWidth / (self._gridWidth + self._xMinimumSpacing)
        self._rowCount = self._availableHeight / (self._gridHeight + self._yMinimumSpacing)

        if (self._rowCount - 1) == 0:
            return

        if (self._columnCount - 1) == 0:
            return

        self._xSpacing = (self._availableWidth - self._gridWidth * self._columnCount) / (self._columnCount - 1)
        self._ySpacing = (self._availableHeight - self._gridHeight * self._rowCount) / (self._rowCount - 1)

        y = self._availableY
        for i in range(self._rowCount):
            for j in range(self._columnCount):
                x = self._availableX + (self._gridWidth + self._xSpacing) * j
                rect = QRect(x, y, self._gridWidth, self._gridHeight)
                gridItem = GridItem(j, i , rect)
                self._map_items.update({gridItem.key(): gridItem})
                self._list_items.append(gridItem)
            y += self._gridHeight + self._ySpacing

        self._availableWidth = self._columnCount * self._gridWidth + (self._columnCount - 1) * self._xSpacing
        self._availableHeight = self._rowCount * self._gridHeight + (self._rowCount - 1) * self._gridHeight
        self._availableRect = QRect(self._availableX, self._availableY, self._availableWidth, self._availableHeight)    



class FixedSpacingGridManager(GridManager):

    def __init__(self):
        super(FixedSpacingGridManager, self).__init__()
        self._availableCount = 0
        self._availableHeight = 0

    def setGridParameters(self, gridWidth, gridHeight, xFixedSpacing, yFixedSpacing, leftMargin, topMargin, rightMargin, bottomMargin):
        self.setGridWidth(gridWidth)
        self.setGridHeight(gridHeight)
        self.setXFixedSpacing(xFixedSpacing)
        self.setYFixedSpacing(yFixedSpacing)
        self.setLeftMargin(leftMargin)
        self.setTopMargin(topMargin)
        self.setRightMargin(rightMargin)
        self.setBottomMargin(bottomMargin)

    def setMargins(self, leftMargin, topMargin, rightMargin, bottomMargin):
        self.setLeftMargin(leftMargin)
        self.setTopMargin(topMargin)
        self.setRightMargin(rightMargin)
        self.setBottomMargin(bottomMargin)

    def generateGrids(self):
        self._list_items = []
        self._map_items = {}
        self._availableWidth = self.geometry().width() - self.leftMargin() - self.rightMargin()
        self._availableHeight = self.geometry().height() - self.topMargin() - self.bottomMargin()
        self._availableX = self.geometry().x() + self.leftMargin()
        self._availableY = self.geometry().y() + self.topMargin()
        self._availableRect = QRect(self._availableX, self._availableY, self._availableWidth, self._availableHeight)

        self._columnCount = self._availableWidth / (self.gridWidth() + self.xFixedSpacing())
        self._rowCount = self._availableHeight / (self.gridHeight() + self.yFixedSpacing())

        self._xSpacing = self.xFixedSpacing()
        self._ySpacing = self.yFixedSpacing()

        y = self._availableY
        for i in range(self._rowCount):
            for j in range(self._columnCount):
                x = self._availableX + (self.gridWidth() + self._xSpacing) * j
                rect = QRect(x, y, self.gridWidth(), self.gridHeight())
                gridItem = GridItem(j, i , rect)
                self._map_items.update({gridItem.key(): gridItem})
                self._list_items.append(gridItem)
            y += self.gridHeight() + self._ySpacing

        self._availableWidth = self._columnCount * self.gridWidth() + (self._columnCount - 1) * self._xSpacing
        self._availableHeight = self._rowCount * self.gridHeight() + (self._rowCount - 1) * self.gridHeight()
        self._availableRect = QRect(self._availableX, self._availableY, self._availableWidth, self._availableHeight)

    def getAvaliableColumnCount(self, width):
        availableWidth = width - self._leftMargin - self._rightMargin
        return availableWidth / (self._gridWidth + self._xFixedSpacing)

    def availableCount(self):
        return self._availableCount

    def getHeightByFixWidth(self, width, itemsCount):
        _availableCount = self.getAvaliableColumnCount(width)
        if _availableCount  == 0:
            self._availableCount  = 1
        else:
            self._availableCount = _availableCount

        if itemsCount % self._availableCount  == 0:
            availableRow = itemsCount / self._availableCount 
        else:
            availableRow = itemsCount / self._availableCount  + 1

        self._availableHeight = self.topMargin() + availableRow * (self.gridHeight() + self.yFixedSpacing()) + self.bottomMargin()

        return self._availableHeight


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
        self._tableItems = []

    def initUI(self):
        self.resize(800, 600)
        self.setStyleSheet(self.style)

    def initConnect(self):
        pass

    def gridManager(self):
        return self._gridManager

    def items(self):
        return self._tableItems

    def addItems(self, items):
        self._tableItems = items

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
        if True:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            for gridItem in self._gridManager.getListItems():
                color = QColor(100, 100, 100, 255)
                painter.fillRect(gridItem.geometry(), color)
        super(IconViewCenterWidget, self).paintEvent(event)



class IconView(QScrollArea):

    requestChangeGridWidth = pyqtSignal(int)
    requestChangeGridHeight = pyqtSignal(int)
    requestChangeXFixedSpacing = pyqtSignal(int)
    requestChangeYFixedSpacing = pyqtSignal(int)
    requestChangeLeftMargin= pyqtSignal(int)
    requestChangeTopMargin = pyqtSignal(int)
    requestChangeRightMargin = pyqtSignal(int)
    requestChangeBottomMargin = pyqtSignal(int)
    requestChangeMargins = pyqtSignal(int, int, int, int)
    requestChangeGridParameters = pyqtSignal(int, int, int, int, int, int, int, int)

    def __init__(self, parent=None):
        super(IconView, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.centerWidget = IconViewCenterWidget(self)
        self.setWidget(self.centerWidget)
        # self.setAlignment(Qt.AlignCenter)
        # self.setWidgetResizable(True)
        self.initData()
        self.initUI()
        self.initConnect()

        self.requestChangeXFixedSpacing.emit(40)
        self.requestChangeGridParameters.emit(50, 50, 30, 30, 30, 30, 30, 0)

    def initData(self):
        pass

    def initUI(self):
        self.setMinimumSize(400, 400)
        self.resize(800, 600)

        self.centerWidget.setGridParameters(100, 100, 10, 10, 10, 10, 10, 0)

        self.tableItems = []
        for i in range(200):
            label = QPushButton("%d" % i, self.centerWidget)
            label.setFixedSize(100, 100)
            self.tableItems.append(label)

        self.centerWidget.addItems(self.tableItems)

    def initConnect(self):
        self.requestChangeXFixedSpacing.connect(self.updateViewByXFixedSpacing)
        self.requestChangeGridParameters.connect(self.updateViewByGridParameters)

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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    iconView = IconView()
    iconView.show()
    sys.exit(app.exec_())
