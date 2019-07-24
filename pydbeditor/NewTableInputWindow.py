from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QLayout,
    QMessageBox,
    QDialog,
    QComboBox,
    QCheckBox,
    QRadioButton
)
from PyQt5.QtCore import Qt
from sqlalchemy import (
    Table,
    Column,
    MetaData,
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

        self.hiddenWidgets = []

        self.columnNames = []
        self.columnTypes = []
        self.notNulls = []
        self.primaryKeys = []
        self.autoIncrements = []
        self.defaults = []

        self.layout = QGridLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.okButton = QPushButton('Создать')
        self.okButton.clicked.connect(self.createTable)

        tableNameLabel = QLabel('Имя таблицы')
        self.tableName = QLineEdit()

        columnNameLabel = QLabel('Имя колонки')
        columnNameLabel.hide()
        self.hiddenWidgets.append(columnNameLabel)

        typeLabel = QLabel('Тип колонки')
        typeLabel.hide()
        self.hiddenWidgets.append(typeLabel)

        defaultLabel = QLabel('По умолчанию')
        defaultLabel.hide()
        self.hiddenWidgets.append(defaultLabel)

        notNullLabel = QLabel('Обязательно')
        notNullLabel.hide()
        self.hiddenWidgets.append(notNullLabel)

        primaryKeyLabel = QLabel('Первичный')
        primaryKeyLabel.hide()
        self.hiddenWidgets.append(primaryKeyLabel)

        autoIncrementLabel = QLabel('Автоинкремент')
        autoIncrementLabel.hide()
        self.hiddenWidgets.append(autoIncrementLabel)

        self.hideWidgets = True

        self.newColumnButton = QPushButton('+')
        self.newColumnButton.clicked.connect(self.addColumn)

        self.lastColumnID = 2

        self.layout.addWidget(tableNameLabel, 0, 0)
        self.layout.addWidget(self.tableName, 1, 0)
        self.layout.addWidget(columnNameLabel, 2, 0)
        self.layout.addWidget(typeLabel, 2, 1)
        self.layout.addWidget(defaultLabel, 2, 2)
        self.layout.addWidget(notNullLabel, 2, 3)
        self.layout.addWidget(primaryKeyLabel, 2, 4)
        self.layout.addWidget(autoIncrementLabel, 2, 5)
        self.layout.addWidget(self.newColumnButton, self.lastColumnID, 0)

        self.layout.addWidget(self.okButton, self.lastColumnID+1, 0, 1, 1)

        self.setLayout(self.layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('Создание таблицы')
        self.resize(500, 300)

    def addColumn(self):
        if self.hideWidgets:
            for e in self.hiddenWidgets:
                e.show()
            self.hideWidgets = False

        newColumnName = QLineEdit()
        self.columnNames.append(newColumnName)

        newColumnType = QComboBox()
        newColumnType.addItems(self.typesStr)
        self.columnTypes.append(newColumnType)

        default = QLineEdit()
        self.defaults.append(default)

        notNull = QCheckBox()
        self.notNulls.append(notNull)

        primaryKey = QRadioButton()
        self.primaryKeys.append(primaryKey)

        autoIncrement = QCheckBox()
        self.autoIncrements.append(autoIncrement)

        self.lastColumnID += 1

        self.layout.addWidget(newColumnName, self.lastColumnID, 0)
        self.layout.addWidget(newColumnType, self.lastColumnID, 1)
        self.layout.addWidget(default, self.lastColumnID, 2)
        self.layout.addWidget(notNull, self.lastColumnID, 3)
        self.layout.addWidget(primaryKey, self.lastColumnID, 4)
        self.layout.addWidget(autoIncrement, self.lastColumnID, 5)

        # Move newColumnButton
        self.layout.removeWidget(self.newColumnButton)
        self.lastColumnID += 1
        self.layout.addWidget(self.newColumnButton, self.lastColumnID, 0)

        # Move okButton
        self.layout.removeWidget(self.okButton)
        self.layout.addWidget(self.okButton, self.lastColumnID+1, 0, 1, 1)

    def createTable(self):
        self.meta = MetaData()
        columns = []
        for name in self.columnNames:
            if name.text() == '':
                QMessageBox.critical(
                    self, 'Ошибка', 'Одно из полей осталось пустым', QMessageBox.Ok, QMessageBox.Ok)
                return
        for (i, name) in enumerate(self.columnNames):
            for j in self.types:
                if j.__name__ == self.columnTypes[i].currentText():
                    type = j
            columns.append(Column(name.text(),
                                  type,
                                  nullable=self.notNulls[i].isChecked(),
                                  primary_key=self.primaryKeys[i].isChecked(),
                                  autoincrement=self.autoIncrements[i].isChecked(),
                                  default=self.defaults[i].text())
                           )
        self.table = Table(self.tableName.text(), self.meta)
        for column in columns:
            self.table.append_column(column)
        self.accept()
