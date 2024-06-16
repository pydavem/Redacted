""" Main program """
import sys
from pathlib import Path
from PyQt6 import QtWidgets
import redactor
import mainWindow


def get_options(window):
    """ Get options from checkboxes """
    return (window.checkBoxIP.isChecked(),
            window.checkBoxLogins.isChecked(),
            window.checkBoxMAC.isChecked(),
            window.checkBoxLogins.isChecked())


def openfile(window):
    """ Open file dialog """
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        None, "Open File", "", "All Files (*)")
    if file_path:
        redactor.redact_file(file_path, *get_options(window))


def openfolder(window):
    """ Open folder dialog """
    folder_path = QtWidgets.QFileDialog.getExistingDirectory(
        None, "Open Folder")
    if folder_path:
        for file_path in Path(folder_path).glob('*'):
            redactor.redact_file(file_path, *get_options(window))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = mainWindow.Ui_MainWindow()
ui.setupUi(MainWindow)

ui.pushButton_openFile.pressed.connect(lambda: openfile(ui))
ui.pushButton_openFolder.pressed.connect(lambda: openfolder(ui))


MainWindow.show()
sys.exit(app.exec())
