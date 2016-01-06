#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ItemManager(QObject):


    def __init__(self, parent=None):
        super(ItemsManager, self).__init__(parent)
