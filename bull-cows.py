import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# ВВЕДЕМ КОНСТАНТЫ
WIN_SPC = 35
WIN_X = 500
WIN_Y = 400

TIT_LABEL = 50

INPNUM_SIZE_X = 60
INPNUM_SIZE_Y = 25

BUT_SIZE_X = 70
BUT_SIZE_Y = 30

TABLE_SIZE_X = 200
TABLE_SIZE_X = 150

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WIN_X, WIN_Y)
        self.setWindowTitle("Быки и коровы")
        self.drawGUI()
        self.seq = []

    def drawGUI(self):
        # Надпись БЫКИ И КОРОВЫ
        self.tlbl = QLabel("БЫКИ И КОРОВЫ", self)
        self.tlbl.setGeometry(0, 0, WIN_X, TIT_LABEL)
        self.tlbl.setAlignment(Qt.AlignCenter)
        self.tlbl.setStyleSheet("border-style: solid;"
                                "border-width: 0px;"
                                "border-color: red;"
                                "font-size:35px;"
                                "font-family: Andale Mono;"
                                "font-weight: bold;")

        # Правила игры
        self.lbl = QLabel("Компьютер загадывает число (ноль в начале быть не может),\n"
                          "а Ваша задача его отгадать. Цифры в числе не повторяются.\n"
                          "Бык - цифра на своем месте.\n"
                          "Корова - цифра есть в числе.", self)
        self.lbl.setGeometry(0, TIT_LABEL, WIN_X, TIT_LABEL + 10)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setStyleSheet("border-style: solid;"
                               "border-width: 0px;"
                               "border-color: green;"
                               "font-family: Courier New, monospace;"
                               "font-size:12px;")

        # Таблица числа, быков и коров
        self.b_clbl = QTableWidget(self)
        self.b_clbl.setGeometry(WIN_SPC,
                                int(WIN_Y / 4 + WIN_SPC / 2),
                                WIN_X - WIN_SPC * 2,
                                int(WIN_Y / 2))
        self.b_clbl.setColumnCount(3)
        self.b_clbl.setHorizontalHeaderLabels(["Число", "Быки", "Коровы"])
        self.b_clbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ввод числа
        self.inpnum = QLineEdit(self)
        self.inpnum.setGeometry(WIN_SPC,
                                WIN_Y - INPNUM_SIZE_Y - WIN_SPC,
                                INPNUM_SIZE_X,
                                INPNUM_SIZE_Y)

        # Кнопка для проверки введенного числа с загаданным
        self.btnOK = QPushButton('Проверить', self)
        self.btnOK.setGeometry(WIN_X - WIN_SPC - BUT_SIZE_X,
                               WIN_Y - BUT_SIZE_Y - WIN_SPC,
                               BUT_SIZE_X,
                               BUT_SIZE_Y)
        self.btnOK.clicked.connect(self.btnOK_clk)
        self.btnOK.setEnabled(False)

        # Кнопка для начала новой игры
        self.ngb = QPushButton('Новая игра', self)
        self.ngb.setGeometry(WIN_X - WIN_SPC * 2 - BUT_SIZE_X * 2,
                             WIN_Y - BUT_SIZE_Y - WIN_SPC,
                             BUT_SIZE_X,
                             BUT_SIZE_Y)
        self.ngb.clicked.connect(self.newGame)

    def normalText(self, w):
        return ''.join(w)

    def btnOK_clk(self):
        n = self.validateNum()  # Введенное число после проверки на валидность
        if not isinstance(n, list):
            self.statusBar().showMessage(n)
            return

        n = self.normalText(n)
        b, c = self.bulls_cows(n)

        # Создание строк в таблице со значениями введенного числа, быков и коров
        rowPosition = self.b_clbl.rowCount()
        self.b_clbl.insertRow(rowPosition)

        self.b_clbl.setItem(rowPosition, 0, QTableWidgetItem(n))
        self.b_clbl.setItem(rowPosition, 1, QTableWidgetItem(str(b)))
        self.b_clbl.setItem(rowPosition, 2, QTableWidgetItem(str(c)))

        if b == 4:
            self.btnOK.setEnabled(False)
            self.statusBar().showMessage("Вы победили! Начните новую игру")

    def newGame(self):
        self.btnOK.setEnabled(True)
        self.b_clbl.setRowCount(0)  # обнуление строк
        self.statusBar().showMessage("Число обновлено!")
        self.genNum()

    def validateNum(self):
        self.statusBar().showMessage("")
        w = self.inpnum.text()

        if not w.isdigit():
            return "Это не число"
        if len(w) != 4:
            return "Только 4 цифры"
        if len(set(w)) != 4:
            return "Цифры без повторов"
        
        return list(w)

    def genNum(self):
        didgits = list("0123456789")
        self.seq = []
        n = random.choice(didgits[1:10])
        self.seq.append(n)
        didgits.remove(n)

        for _ in range(3):
            n = random.choice(didgits)
            self.seq.append(n)
            didgits.remove(n)

        print(self.seq)  # для отладки

    def bulls_cows(self, guess):
        s = self.seq
        y = list(guess)

        b = sum(1 for i in range(4) if y[i] == s[i])
        c = sum(1 for i in y if i in s) - b

        return b, c

app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()
