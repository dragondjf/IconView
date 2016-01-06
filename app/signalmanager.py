#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject


class SignalManager(QObject):

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)


signalManger = SignalManager()
