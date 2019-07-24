from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton
)
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine


class ConnectToDBInput(QDialog):
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
        self.engine = create_engine(
            f'{self.dbDialect.currentText()}://{self.username.text()}:{self.password.text()}@{self.address.text()}/{self.dbName.text()}'
        )
        self.conn = self.engine.connect()
        self.accept()
