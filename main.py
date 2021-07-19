from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("template.ui")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    app.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
