import os,sys
import string

"""
path = os.path.abspath(os.path.dirname(__file__))
proc = subprocess.Popen([sys.executable, '-'] + extra, stdin=subprocess.PIPE, cwd=path)
code = str(self.ui.codeView.toPlainText()).encode('UTF-8')
proc.stdin.write(code)
proc.stdin.close()
"""
fn = "isfile003.py"
path = r"D:/GitHub/gitpython/twoFirst01/qtgui4/Files/"
file = os.path.join(path, fn)
files = "D:/GitHub/gitpython/twoFirst01/qtgui4/Files/isfile003.py"
extra = []
extra.append("pyqt4")
extra.append("native")
if sys.platform.startswith('win'):
    os.spawnl(os.P_NOWAIT, sys.executable, '"' + sys.executable + '"', '"' + fn + '"', *extra)
    print  sys.executable,file
else:
    os.spawnl(os.P_NOWAIT, sys.executable, sys.executable, files)
print "11111"