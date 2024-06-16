""" Main program """
import sys
from pathlib import Path
from PyQt6 import QtWidgets, QtCore
import redactor
import mainWindow_ui


def save_options(window):
    """ Save options to file """
    QtCore.QSettings().setValue('options', (window.checkBoxIP.isChecked(),
                                            window.checkBoxLogins.isChecked(),
                                            window.checkBoxMAC.isChecked(),
                                            window.checkBoxLogins.isChecked()))


def read_options(window):
    """ Read options from file """
    options = QtCore.QSettings().value('options', (True, True, True, True))
    window.checkBoxIP.setChecked(options[0])
    window.checkBoxLogins.setChecked(options[1])
    window.checkBoxMAC.setChecked(options[2])
    window.checkBoxLogins.setChecked(options[3])


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
        for file_path in Path(folder_path).glob('*.txt'):
            redactor.redact_file(file_path, *get_options(window))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = mainWindow_ui.Ui_MainWindow()
ui.setupUi(MainWindow)
read_options(ui)

ui.pushButton_openFile.pressed.connect(lambda: openfile(ui))
ui.pushButton_openFolder.pressed.connect(lambda: openfolder(ui))


MainWindow.show()

exitcode = app.exec()
if not exitcode:
    save_options(ui)
sys.exit(exitcode)
