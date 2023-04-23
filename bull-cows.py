# Импортируем все, что нам нужно
import random
import sys
from PyQt5.QtWidgets import QApplication,\
                            QMainWindow,\
                            QPushButton,\
                            QLabel, QLineEdit,\
                            QTableWidget, QTableWidgetItem,\
                            QHeaderView
                            
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
        
        self.setFixedSize(WIN_X,WIN_Y)
        self.setWindowTitle("Быки и коровы")
        self.drawGUI()
        
    def drawGUI(self):
        
        # Надпись БЫКИ И КОРОВЫ
        self.tlbl = QLabel("БЫКИ И КОРОВЫ", self)
        self.tlbl.setGeometry(0,0,WIN_X,TIT_LABEL)
        self.tlbl.setAlignment(Qt.AlignCenter)
        self.tlbl.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: red;"
                                 "font-size:35px;"
                                 "font-family: Andale Mono;"
                                 "font-weight: bold;")
        # Правила игры
        self.lbl =  QLabel("Компьтер загадывает число(ноль в начале быть не может),\
                           \n а Ваша задача его отгадать. Цифры в числе не повторяются.\
                           \n Бык - цифра на своем месте.\n Корова - цифра есть в числе.", self)
        self.lbl.setGeometry(0,TIT_LABEL,WIN_X,TIT_LABEL+10)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setStyleSheet("border-style: solid;"
                                 "border-width: 0px;"
                                 "border-color: green;"
                                 "font-family: Courier New, monospace;"
                                 "font-size:12px;")
        
        
        # Таблица числа, быков и коров
        self.b_clbl = QTableWidget(self)
        self.b_clbl.setGeometry(WIN_SPC,
                                WIN_Y/4+WIN_SPC/2,
                                WIN_X-WIN_SPC*2
                                ,WIN_Y/2)
        #self.b_clbl.setStyleSheet("border-style: solid;"
        #                          "border-width: 1px;"
        #                          "border-color: blue;")
        
        self.b_clbl.setColumnCount(3)
        self.b_clbl.setHorizontalHeaderLabels(["Число", "Быки", "Коровы"])
 
        self.b_clbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        
        # Ввод числа
        self.inpnum = QLineEdit(self)
        self.inpnum.setGeometry(WIN_SPC,
                                WIN_Y-INPNUM_SIZE_Y-WIN_SPC,
                                INPNUM_SIZE_X,
                                INPNUM_SIZE_Y)
        
        
        # Кнопка для проверки введенного числа с загаданным
        self.btnOK = QPushButton('Проверить', self)
        self.btnOK.setGeometry(WIN_X-WIN_SPC-BUT_SIZE_X,
                               WIN_Y-BUT_SIZE_Y-WIN_SPC,
                               BUT_SIZE_X,
                               BUT_SIZE_Y)
        self.btnOK.clicked.connect(self.btnOK_clk)
        self.btnOK.setEnabled(False)
        
        # Кнопка для начала новой игры
        self.ngb = QPushButton('Новая игра', self)
        self.ngb.setGeometry(WIN_X-WIN_SPC*2-BUT_SIZE_X*2,
                               WIN_Y-BUT_SIZE_Y-WIN_SPC,
                               BUT_SIZE_X,
                               BUT_SIZE_Y)
        self.ngb.clicked.connect(self.newGame)
        
    # перевод значений из ['1','2','3','4'] в 1234 для корректного отображения в таблице
    def normalText(self):
        aa = self.validateNum()
        a = map(str, aa)
        a = ''.join(a)
        a = str(a)
        return a
    
    
    def btnOK_clk(self):
        n = self.normalText()               # Введенное число после проверки на валидность

        b = self.bulls_cows()[0]                # Быки
        c = self.bulls_cows()[1]                # Коровы
            
        # Перевод значений в str для отображения в таблице
        x = str(n)                           
        y = str(b)
        z = str(c)
        
        #a1 = self.seq
        #a = str(a1)
        
        # Создание строк в таблице со значениями введенного числа, быков и коров
        
        rowPosition = self.b_clbl.rowCount()                               
        self.b_clbl.insertRow(rowPosition)  
        
        self.b_clbl.setItem(rowPosition, 0, QTableWidgetItem(x))
        self.b_clbl.setItem(rowPosition, 1, QTableWidgetItem(y))
        self.b_clbl.setItem(rowPosition, 2, QTableWidgetItem(z))
        
        #!!!!!!!!!!!
        # строка с загаданным числом для отладки
        #self.b_clbl.setItem(rowPosition, 3, QTableWidgetItem(a))
        #!!!!!!!!!!!
        
        #self.inpnum.clear()
        #self.statusBar().showMessage("")
        
    def newGame(self):
        
        self.btnOK.setEnabled(True)
        self.b_clbl.setRowCount(0);                         # обнуление строк
        self.statusBar().showMessage("Число обновлено!")
        self.genNum() 


    # функция проверки ввода на валидность
    def validateNum(self):
        self.statusBar().showMessage("")
        w = self.inpnum.text()
        # попытка перевсти введенное значение в int
        try:
            w = int(w)
        # если не вышло, присвоить любое другое значение
        except:
            #print('The variable is not a number')
            w = "Это не число"
        finally:
            if type(w) == int:
                w = int(w) 
                
            
        if len(str(w)) != 4:
            #print("Только 4 цифры")
            w = "Только 4 цифры"
        
        elif len(set(str(w))) != 4:
            #print("Только 4 цифры, без повторов")
            w = "Цифры без повторов"
            
        w = list(str(w))
        return w
        

    
    
    def genNum(self):                                           
        didgits = list("0123456789")
        self.seq = []
        n = random.choice(didgits[1:10])
        self.seq.append(n)
        didgits.remove(n)
        
        for i in range(3):
            n = random.choice(didgits)
            self.seq.append(n)
            didgits.remove(n)
        
            #print(type(self.seq))
        print (self.seq)
        
        # для отладки последовательность будет 1234
        #!!!!!!!!!!!!!!!!!!!!
        #self.seq = ['1','2','3','4']
        #!!!!!!!!!!!!!!!!!!!!                                                       
    
    
    def bulls_cows(self):
        s = self.seq
        y1 = self.validateNum() 
        y = list(str(y1))
        # расчет быков и коров в загаданном числе
                                       
        b = 0 
        c = 0                                      
        for i in range(4):  
            if y1[i] == s[i]: 
                b += 1  
        #print(str(b)+"bulls") 
 
        for i in y:                          
            if (i in set(s)) == True:                          
                c += 1 

        if b != 0:
             c = int(c) - int(b)                   
        #print(str(c)+"cows") 
        
        # выключение кнокпи если число быков равно 4(победа)
        if b == 4:
            self.btnOK.setEnabled(False)
            self.statusBar().showMessage("Вы победили! Начните новую игру")
         
        # возврат кол-ва быков и коров в виде списка
        b_c = [b,c]
        return b_c
        
        



app = QApplication(sys.argv)
win = MainWindow()
win.show()
print(WIN_X, WIN_Y)
app.exec()