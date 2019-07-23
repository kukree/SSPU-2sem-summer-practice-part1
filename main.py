from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QGridLayout,
    QTabWidget,
    QTableWidget,
    QPushButton,
    QGroupBox,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QDialog,
    QMessageBox,
    QFormLayout,
    QLayout,
    QComboBox
)
from PyQt5.QtCore import Qt
import sys
import sqlalchemy


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        addButton = QPushButton('Добавить')
        vbox.addWidget(addButton)

        editButton = QPushButton('Редактировать')
        vbox.addWidget(editButton)

        removeButton = QPushButton('Удалить')
        vbox.addWidget(removeButton)

        connectToDBButton = QPushButton('Подключиться к базе данных')
        connectToDBButton.clicked.connect(self.showConnectToDBWindow)
        vbox.addWidget(connectToDBButton)

        groupBox = QGroupBox('Редактирование')
        groupBox.setLayout(vbox)

        self.employeesTable = EmployeesTable()  # TEMP

        addTabButton = QPushButton('+')
        addTabButton.setFixedSize(35, 30)
        addTabButton.clicked.connect(self.createTable)

        self.tabs = QTabWidget()
        self.tabs.setCornerWidget(addTabButton)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.tabs, 0, 1, 5, 5)
        self.mainLayout.addWidget(groupBox, 0, 6)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('DBEdit')
        self.resize(1000, 500)
        self.show()

    def showConnectToDBWindow(self):
        dbInput = DataBaseInput(self)
        response = dbInput.exec_()
        if response == QDialog.Accepted:
            self.dbConn = dbInput.conn
            self.dbEngine = dbInput.engine
            tables = self.dbEngine.table_names()
            for table in tables:
                self.tabs.addTab(self.employeesTable, table)

    def createTable(self):
        newTableInput = NewTableInput(self)
        response = newTableInput.exec_()
        if response == QDialog.Accepted:
            print('Meow!')  # TEMP


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


class DataBaseInput(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initWindow()

    def initWindow(self):
        layout = QFormLayout()

        addressLabel = QLabel('Адрес сервера')
        self.address = QLineEdit()

        usernameLabel = QLabel('Имя пользователя')
        self.username = QLineEdit()

        passwordLabel = QLabel('Пароль')
        self.password = QLineEdit()

        dbNameLabel = QLabel('Название базы данных')
        self.dbName = QLineEdit()

        dbDialectLabel = QLabel('Диалект SQL')
        self.dbDialect = QComboBox()
        self.dbDialect.addItems(['sqlite', 'postgresql', 'mysql', 'oracle', 'mssql'])

        okButton = QPushButton('Подключиться')
        okButton.clicked.connect(self.connectToDB)

        layout.addRow(addressLabel, self.address)
        layout.addRow(usernameLabel, self.username)
        layout.addRow(passwordLabel, self.password)
        layout.addRow(dbNameLabel, self.dbName)
        layout.addRow(dbDialectLabel, self.dbDialect)
        layout.addRow(okButton)
        layout.setLabelAlignment(Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('Подключение к базе данных')
        self.resize(300, 250)

    def connectToDB(self):
        self.engine = sqlalchemy.create_engine(
            f'{self.dbDialect.currentText()}://{self.username.text()}:{self.password.text()}@{self.address.text()}/{self.dbName.text()}'
        )
        self.conn = self.engine.connect()
        self.accept()


# TODO: Удалить все автосозданные вкладки снизу (они будут заменены таблицами в базе данных)
# TODO: Создать класс для новой таблицы и ее вывода в окне вкладок

# TEMP CLASS
class EmployeesTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Сотрудники'
        labels = ['Код', 'ФИО', 'Возраст', 'Пол', 'Адрес', 'Телефон', 'Паспортные данные', 'Код должности']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
