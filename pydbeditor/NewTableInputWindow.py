from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QLayout,
    QMessageBox,
    QDialog
)
from PyQt5.QtCore import Qt


class NewTableInput(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initWindow()

    def initWindow(self):
        self.names = []

        self.layout = QGridLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.okButton = QPushButton('Создать')
        self.okButton.clicked.connect(self.createTable)

        tableNameLabel = QLabel('Имя таблицы')
        self.tableName = QLineEdit()

        self.newColumnLabel = QLabel('Новая колонка')
        self.newColumnButton = QPushButton('+')
        self.newColumnButton.clicked.connect(self.addColumn)

        self.lastColumnID = 1

        self.layout.addWidget(tableNameLabel, 0, 0)
        self.layout.addWidget(self.tableName, 1, 0)
        self.layout.addWidget(self.newColumnLabel, 0, self.lastColumnID)
        self.layout.addWidget(self.newColumnButton, 1, self.lastColumnID)

        self.layout.addWidget(self.okButton, 2, 0, 1, self.lastColumnID+1)

        self.setLayout(self.layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('Создание таблицы')
        self.resize(500, 300)

    def addColumn(self):
        self.layout.removeWidget(self.newColumnLabel)
        self.layout.removeWidget(self.newColumnButton)
        newColumnNameLabel = QLabel('Имя колонки')
        newColumnName = QLineEdit()
        self.names.append(newColumnName)
        self.lastColumnID += 1
        self.layout.addWidget(newColumnNameLabel, 0, self.lastColumnID)
        self.layout.addWidget(newColumnName, 1, self.lastColumnID)
        self.lastColumnID += 1
        self.layout.addWidget(self.newColumnLabel, 0, self.lastColumnID)
        self.layout.addWidget(self.newColumnButton, 1, self.lastColumnID)
        self.layout.removeWidget(self.okButton)
        self.layout.addWidget(self.okButton, 2, 0, 1, self.lastColumnID + 1)

    def createTable(self):
        for name in self.names:
            if name.text() == '':
                QMessageBox.critical(
                    self, 'Ошибка', 'Одно из полей осталось пустым', QMessageBox.Ok, QMessageBox.Ok)
                return
        self.accept()
