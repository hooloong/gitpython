#!/usr/bin/env python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)

web = QWebView()
# web.load(QUrl("http://www.baidu.com"))
web.load(QUrl("lines.html"))
web.show()

sys.exit(app.exec_())