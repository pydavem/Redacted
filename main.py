""" Main program """
import sys
from pathlib import Path
from PyQt6 import QtWidgets, QtCore
import redactor
from results import Results
import mainWindow_ui


def save_options(window):
    """ Save options to file """
    QtCore.QSettings().setValue('options', (window.checkBoxIP.isChecked(),
                                            window.checkBoxMachines.isChecked(),
                                            window.checkBoxMAC.isChecked(),
                                            window.checkBoxLogins.isChecked()))


def read_options(window):
    """ Read options from file """
    options = QtCore.QSettings().value('options', (True, True, True, True))
    window.checkBoxIP.setChecked(options[0])
    window.checkBoxMachines.setChecked(options[1])
    window.checkBoxMAC.setChecked(options[2])
    window.checkBoxLogins.setChecked(options[3])


def get_options(window):
    """ Get options from checkboxes """
    return (window.checkBoxIP.isChecked(),
            window.checkBoxLogins.isChecked(),
            window.checkBoxMAC.isChecked(),
            window.checkBoxLogins.isChecked())


def add_results(window, res: Results):
    """ Add results to table """
    i = window.tableWidget_results.rowCount()
    window.tableWidget_results.setRowCount(i + 1)
    window.tableWidget_results.setItem(
        i, 0, QtWidgets.QTableWidgetItem(str(res.ips)))
    window.tableWidget_results.setItem(
        i, 1, QtWidgets.QTableWidgetItem(str(res.macs)))
    window.tableWidget_results.setItem(
        i, 2, QtWidgets.QTableWidgetItem(str(res.machines)))
    window.tableWidget_results.setItem(
        i, 3, QtWidgets.QTableWidgetItem(str(res.logins)))
    window.tableWidget_results.setItem(
        i, 4, QtWidgets.QTableWidgetItem(res.file))


def openfile(window):
    """ Open file dialog """
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        None, "Open File", "", "All Files (*)")
    if file_path:
        res = Results()
        res = redactor.redact_file(file_path, *get_options(window))
        if not res is None:
            add_results(window, res)


def openfolder(window):
    """ Open folder dialog """
    folder_path = QtWidgets.QFileDialog.getExistingDirectory(
        None, "Open Folder")
    if folder_path:
        res = Results()
        for file_path in Path(folder_path).glob('*.txt'):
            res = redactor.redact_file(file_path, *get_options(window))
            if not res is None:
                add_results(window, res)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = mainWindow_ui.Ui_MainWindow()
ui.setupUi(MainWindow)
read_options(ui)

ui.pushButton_openFile.pressed.connect(lambda: openfile(ui))
ui.pushButton_openFolder.pressed.connect(lambda: openfolder(ui))
ui.tableWidget_results.setHorizontalHeaderLabels(
    ['IPs', 'MACs', 'Machines', 'Logins', 'File'])

MainWindow.show()

exitcode = app.exec()
if not exitcode:
    save_options(ui)
sys.exit(exitcode)
