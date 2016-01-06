#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .iconitem import IconItem
import random


class ItemManager(QObject):

    itemRemoved = pyqtSignal(unicode)
    itemsChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super(ItemManager, self).__init__(parent)
        self.initData()

        self.timer = QTimer()
        self.index = 0
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.removeRandomItem)
        self.timer.start()

    def initData(self):
        self._items = []
        self._map_items = {}
        for i in range(2000):
            key = "%d" % i
            iconItem = IconItem(key, self.parent())
            iconItem.setText(key)
            iconItem.selfRemoved.connect(self.removeItemByKey)
            self._items.append(iconItem)
            self._map_items.update({key: iconItem})

    def initConnect(self):
        pass

    def items(self):
        return self._items

    def removeRandomItem(self):
        self.index += 1
        print("removeRandomItem", self.index)
        key = "%d" % self.index
        self.removeItemByKey(key)

    def removeItemByKey(self, key):
        if key in self._map_items:
            iconItem = self._map_items[key]
            iconItem.deleteLater()
            self._map_items.pop(key)
            self._items.remove(iconItem)
            self.itemsChanged.emit(self._items)
