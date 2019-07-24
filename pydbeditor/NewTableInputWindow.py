from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QLayout,
    QMessageBox,
    QDialog,
    QComboBox
)
from PyQt5.QtCore import Qt
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time
)


class NewTableInput(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initWindow()

    def initWindow(self):
        self.types = [
            BigInteger,
            Boolean,
            Date,
            DateTime,
            Float,
            Integer,
            Numeric,
            SmallInteger,
            String,
            Text,
            Time
        ]
        self.typesStr = [str(i.__name__) for i in self.types]
        self.columnNames = []
        self.columnTypes = []

        self.layout = QGridLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.okButton = QPushButton('Создать')
        self.okButton.clicked.connect(self.createTable)

        tableNameLabel = QLabel('Имя таблицы')
        self.tableName = QLineEdit()

        self.columnNameLabel = QLabel('Имя колонки')
        self.columnNameLabel.hide()  # Hide while newColumnButton is not clicked

        self.typeLabel = QLabel('Тип колонки')
        self.typeLabel.hide()  # Hide while newColumnButton is not clicked

        self.labelsHidden = True

        self.newColumnButton = QPushButton('+')
        self.newColumnButton.clicked.connect(self.addColumn)

        self.lastColumnID = 2

        self.layout.addWidget(tableNameLabel, 0, 0)
        self.layout.addWidget(self.tableName, 1, 0)
        self.layout.addWidget(self.columnNameLabel, 2, 0)
        self.layout.addWidget(self.typeLabel, 2, 1)
        self.layout.addWidget(self.newColumnButton, self.lastColumnID, 0)

        self.layout.addWidget(self.okButton, self.lastColumnID+1, 0, 1, 1)

        self.setLayout(self.layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('Создание таблицы')
        self.resize(500, 300)

    def addColumn(self):
        if self.labelsHidden:
            self.labelsHidden = False
            self.columnNameLabel.show()
            self.typeLabel.show()

        newColumnName = QLineEdit()
        self.columnNames.append(newColumnName)
        newColumnType = QComboBox()
        newColumnType.addItems(self.typesStr)
        self.columnTypes.append(newColumnType)

        self.lastColumnID += 1

        self.layout.addWidget(newColumnName, self.lastColumnID, 0)
        self.layout.addWidget(newColumnType, self.lastColumnID, 1)

        # Move newColumnButton
        self.layout.removeWidget(self.newColumnButton)
        self.lastColumnID += 1
        self.layout.addWidget(self.newColumnButton, self.lastColumnID, 0)

        # Move okButton
        self.layout.removeWidget(self.okButton)
        self.layout.addWidget(self.okButton, self.lastColumnID+1, 0, 1, 1)

    def createTable(self):
        for name in self.columnNames:
            if name.text() == '':
                QMessageBox.critical(
                    self, 'Ошибка', 'Одно из полей осталось пустым', QMessageBox.Ok, QMessageBox.Ok)
                return
        self.accept()
