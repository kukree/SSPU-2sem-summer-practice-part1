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
    QMessageBox
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
        layout = QGridLayout()

        addressLabel = QLabel('Адрес сервера')
        self.address = QLineEdit()

        usernameLabel = QLabel('Имя пользователя')
        self.username = QLineEdit()

        passwordLabel = QLabel('Пароль')
        self.password = QLineEdit()

        dbNameLabel = QLabel('Название базы данных')
        self.dbName = QLineEdit()

        dbDialectLabel = QLabel('Диалект SQL')
        self.dbDialect = QLineEdit()

        okButton = QPushButton('Подключиться')
        okButton.clicked.connect(self.connectToDB)

        layout.addWidget(addressLabel, 0, 0)
        layout.addWidget(self.address, 0, 1)
        layout.addWidget(usernameLabel, 1, 0)
        layout.addWidget(self.username, 1, 1)
        layout.addWidget(passwordLabel, 2, 0)
        layout.addWidget(self.password, 2, 1)
        layout.addWidget(dbNameLabel, 3, 0)
        layout.addWidget(self.dbName, 3, 1)
        layout.addWidget(dbDialectLabel, 4, 0)
        layout.addWidget(self.dbDialect, 4, 1)
        layout.addWidget(okButton, 5, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('Подключение к базе данных')
        self.resize(300, 300)

    def connectToDB(self):
        self.engine = sqlalchemy.create_engine(
            f'{self.dbDialect.text()}://{self.username.text()}:{self.password.text()}@{self.address.text()}/{self.dbName.text()}'
        )
        self.conn = self.engine.connect()
        self.accept()


# TODO: Удалить все автосозданные вкладки снизу (они будут заменены таблицами в базе данных)
# TODO: Создать класс для новой таблицы и ее вывода в окне вкладок
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


class PostsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Должности'
        labels = ['Код должности', 'Наименование должности', 'Оклад', 'Обязанности', 'Требования']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


class ProductsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Товары'
        labels = ['Код товара', 'Код типа', 'Производитель', 'Наименование', 'Условия хранения', 'Упаковка',
                  'Срок годности']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


class ProductsTypesTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Типы товаров'
        labels = ['Код типа', 'Наименование', 'Описание', 'Особенности']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


class SuppliersTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Поставщики'
        labels = ['Код поставщика', 'Наименование', 'Адрес', 'Телефон', 'Код поставляемого товара']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


class CustomersTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Заказчики'
        labels = ['Код заказчика', 'Наименование', 'Адрес', 'Телефон', 'Код товара']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


class StockTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.name = 'Склад'
        labels = ['Дата поступления', 'Дата заказа', 'Дата отправки', 'Код товара', 'Код поставщика', 'Код заказчика'
                  'Способ поставки', 'Обьем', 'Цена', 'Код сотрудника']
        self.setColumnCount(len(labels))
        self.setRowCount(1)
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
