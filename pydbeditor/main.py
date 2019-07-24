from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QGridLayout,
    QTabWidget,
    QTableWidget,
    QPushButton,
    QGroupBox,
    QVBoxLayout,
    QDialog,
)
from NewTableInputWindow import NewTableInput
from ConnectToDBWindow import ConnectToDBInput
import sys


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
        dbInput = ConnectToDBInput(self)
        response = dbInput.exec_()
        if response == QDialog.Accepted:
            self.dbConn = dbInput.conn
            self.dbEngine = dbInput.engine
            self.loadTables()

    def createTable(self):
        newTableInput = NewTableInput(self)
        response = newTableInput.exec_()
        if response == QDialog.Accepted:
            meta = newTableInput.meta
            meta.create_all(self.dbEngine)
            self.tabs.clear()
            tables = self.dbEngine.table_names()
            for table in tables:
                self.tabs.addTab(QWidget(), table)

    def loadTables(self):
        tables = self.dbEngine.table_names()
        for table in tables:
            self.tabs.addTab(QWidget(), table)


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
