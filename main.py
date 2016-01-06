#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from views import IconView


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    iconView = IconView()
    iconView.show()
    sys.exit(app.exec_())
