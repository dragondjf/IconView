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

    def geometry(self):
        return self._geometry

    def setGeometry(self, rect):
        self._geometry = rect

    def key(self):
        return "%s-%s" % (self._geometry.x(), self._geometry.y())


class GridManager(QObject):

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

    def gridWidth(self):
        return self._gridWidth

    def gridHeight(self):
        return self._gridHeight

    def xMinimumSpacing(self):
        return self._xMinimumSpacing

    def yMinimumSpacing(self):
        return self._yMinimumSpacing

    def xFixedSpacing(self):
        return self._xFixedSpacing

    def yFixedSpacing(self):
        return self._yFixedSpacing

    def leftMargin(self):
        return self._leftMargin

    def topMargin(self):
        return self._topMargin

    def rightMargin(self):
        return self._rightMargin

    def bottomMargin(self):
        return self._bottomMargin

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
    """docstring for DynamicSpacingGridManager"""
    def __init__(self):
        super(FixedSpacingGridManager, self).__init__()

    def initGridParameter(self, gridWidth, gridHeight, xFixedSpacing, yFixedSpacing, leftMargin, topMargin, rightMargin, bottomMargin):
        self._gridWidth = gridWidth
        self._gridHeight = gridHeight
        self._xFixedSpacing = xFixedSpacing
        self._yFixedSpacing = yFixedSpacing
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

        self._columnCount = self._availableWidth / (self._gridWidth + self._xFixedSpacing)
        self._rowCount = self._availableHeight / (self._gridHeight + self._yFixedSpacing)

        self._xSpacing = self._xFixedSpacing
        self._ySpacing = self._yFixedSpacing

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
    
    def getAvaliableColumnCount(self, width):
        availableWidth = width - self._leftMargin - self._rightMargin
        return availableWidth / (self._gridWidth + self._xFixedSpacing)

    def getHeightByFixWiuth(self, width, itemsCount):
        availableCount = self.getAvaliableColumnCount(width)
        if availableCount == 0:
            availableCount = 1

        if itemsCount % availableCount == 0:
            availableRow = itemsCount / availableCount
        else:
            availableRow = itemsCount / availableCount + 1

        availableHeight = self.topMargin() + availableRow * (self.gridHeight() + self.yFixedSpacing()) + self.bottomMargin()

        return availableHeight


class IconView(QFrame):
    """docstring for MainWindow"""
    def __init__(self, parent=None):
        super(IconView, self).__init__(None)
        self.parent = parent
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        self.gridManager = FixedSpacingGridManager()
        self.gridManager.initGridParameter(100, 100, 10, 10, 10, 10, 10, 10)

    def initUI(self):
        self.resize(800, 600)
        self.tableItems = []
        for i in range(200):
            label = QLabel("%d" % i, self)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(100, 100)
            self.tableItems.append(label)

    def initConnect(self):
        pass

    def reLayoutItemsByRect(self, rect):
        self.gridManager.generateGridsByRect(rect)
        items = self.gridManager.getListItems()
        for tableItem in self.tableItems:
            index = self.tableItems.index(tableItem)
            if index < len(items):
                gridItem =items[index]
                tableItem.setGeometry(gridItem.geometry())

    def paintEvent(self, event):
        if True:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            for gridItem in self.gridManager.getListItems():
                color = QColor(100, 100, 100, 255)
                painter.fillRect(gridItem.geometry(), color)
        super(IconView, self).paintEvent(event)

    def resizeEvent(self, event):
        availableHeight = self.gridManager.getHeightByFixWiuth(event.size().width(), len(self.tableItems))
        rect = QRect(0, 0, event.size().width(), availableHeight)
        self.reLayoutItemsByRect(rect)
        super(IconView, self).resizeEvent(event)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = IconView()
    main.show()
    sys.exit(app.exec_())
