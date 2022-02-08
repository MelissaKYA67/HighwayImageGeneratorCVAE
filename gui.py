import sys

from src.generate_image import gen_img
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QRadioButton,
    QButtonGroup,
    QMessageBox
)


def popup(text):
    mbox = QMessageBox()

    mbox.setWindowTitle("Input Conditions")
    mbox.setText(text)

    mbox.setStandardButtons(QMessageBox.Ok)
    mbox.exec_()


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.choice1 = None
        self.choice2 = None

        self.resize(957, 800)
        self.setWindowTitle("Highway Image Generator")

        x1 = 620
        x2 = 654

        self.error = QLabel(self)
        self.error.setGeometry(x2, 730, 300, 50)
        self.error.setFont(QFont('Arial', 10))
        self.error.setStyleSheet("color: red")

        bord = QLabel(self)
        bord.setGeometry(x1, 0, 337, 800)
        bord.setStyleSheet("border: 4px solid black;")

        lab1 = QLabel("Directions & Bearings:", self)
        lab1.setFont(QFont('Arial', 20))
        lab1.setGeometry(x2, 40, 300, 50)

        bg1 = QButtonGroup(self)

        rbtn11 = QRadioButton(">N80e-3°W", self)
        rbtn11.setGeometry(x2, 80, 300, 50)
        rbtn11.setFont(QFont('Arial', 12))
        rbtn11.toggled.connect(self.update_choice1)

        rbtn12 = QRadioButton("N50e-3°W to N79e-3°W", self)
        rbtn12.setGeometry(x2, 120, 300, 50)
        rbtn12.setFont(QFont('Arial', 12))
        rbtn12.toggled.connect(self.update_choice1)

        rbtn13 = QRadioButton("N30e-3°W to N49e-3°W", self)
        rbtn13.setGeometry(x2, 160, 300, 50)
        rbtn13.setFont(QFont('Arial', 12))
        rbtn13.toggled.connect(self.update_choice1)

        rbtn14 = QRadioButton("0°", self)
        rbtn14.setGeometry(x2, 200, 300, 50)
        rbtn14.setFont(QFont('Arial', 12))
        rbtn14.toggled.connect(self.update_choice1)


        rbtn15 = QRadioButton(">N80e-3°E", self)
        rbtn15.setGeometry(x2, 240, 300, 50)
        rbtn15.setFont(QFont('Arial', 12))
        rbtn15.toggled.connect(self.update_choice1)

        rbtn16 = QRadioButton("N50e-3°E to N79e-3°E", self)
        rbtn16.setGeometry(x2, 280, 300, 50)
        rbtn16.setFont(QFont('Arial', 12))
        rbtn16.toggled.connect(self.update_choice1)

        rbtn17 = QRadioButton("N30e-3°E to N49e-3°E", self)
        rbtn17.setGeometry(x2, 320, 300, 50)
        rbtn17.setFont(QFont('Arial', 12))
        rbtn17.toggled.connect(self.update_choice1)

        bg1.addButton(rbtn11)
        bg1.addButton(rbtn12)
        bg1.addButton(rbtn13)
        bg1.addButton(rbtn14)
        bg1.addButton(rbtn15)
        bg1.addButton(rbtn16)
        bg1.addButton(rbtn17)

        lab2 = QLabel("Ego-car Position:", self)
        lab2.setGeometry(x2, 390, 300, 50)
        lab2.setFont(QFont('Arial', 20))

        bg2 = QButtonGroup(self)

        rbtn21 = QRadioButton("Left", self)
        rbtn21.setGeometry(x2, 430, 300, 50)
        rbtn21.setFont(QFont('Arial', 12))
        rbtn21.toggled.connect(self.update_choice2)

        rbtn22 = QRadioButton("Middle", self)
        rbtn22.setGeometry(x2, 470, 300, 50)
        rbtn22.setFont(QFont('Arial', 12))
        rbtn22.toggled.connect(self.update_choice2)

        rbtn23 = QRadioButton("Right", self)
        rbtn23.setGeometry(x2, 510, 300, 50)
        rbtn23.setFont(QFont('Arial', 12))
        rbtn23.toggled.connect(self.update_choice2)

        bg2.addButton(rbtn21)
        bg2.addButton(rbtn22)
        bg2.addButton(rbtn23)

        btn_gen = QPushButton("GENERATE", self)
        btn_gen.setGeometry(x2+25, 620, 200, 100)
        btn_gen.setStyleSheet("background-color: black; color: white")
        btn_gen.setFont(QFont('Arial', 20))
        btn_gen.clicked.connect(self.generate_button)

        # Display image
        self.lab_pic = QLabel(self)

        self.dict_dnb = {'>N80e-3°W': 0,
                    'N50e-3°W to N79e-3°W': 1,
                    'N30e-3°W to N49e-3°W': 2,
                    '0°': 3,
                    '>N80e-3°E': 4,
                    'N50e-3°E to N79e-3°E': 5,
                    'N30e-3°E to N49e-3°E': 6}

        self.dict_ego = {'Left': 0,
                         'Middle': 1,
                         'Right': 2}

        self.choice1_text = None
        self.choice2_text = None

    def update_choice1(self, value):
        rbtn = self.sender()

        if rbtn.isChecked() == True:
            self.choice1_text = rbtn.text()
            self.choice1 = self.dict_dnb[rbtn.text()]

    def update_choice2(self, value):
        rbtn = self.sender()

        if rbtn.isChecked() == True:
            self.choice2_text = rbtn.text()
            self.choice2 = self.dict_ego[rbtn.text()]

    def generate_button(self, value):

        self.error.setText("")

        # Display error message if both radio buttons or one of them is not checked
        if (self.choice1_text is None) or (self.choice2_text is None):
            self.error.setText("Please select both conditions.")
            return
        else:
            desc = "Selected input conditions:\n\n"
            desc += "Directions and Bearings: "
            desc += self.choice1_text + "\n"
            desc += "Ego-car Position: "
            desc += self.choice2_text + "\n\n"
            desc += "Generating image...\nPlease wait for a maximum of 4 second(s)"
            popup(desc)
            self.display_Image()

    def display_Image(self):

        if self.choice1 == 0 and self.choice2 == 0:
            gen_img(2)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 0 and self.choice2 == 1:
            gen_img(9)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 0 and self.choice2 == 2:
            gen_img(16)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 1 and self.choice2 == 0:
            gen_img(1)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 1 and self.choice2 == 1:
            gen_img(8)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 1 and self.choice2 == 2:
            gen_img(15)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 2 and self.choice2 == 0:
            gen_img(0)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 2 and self.choice2 == 1:
            gen_img(7)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 2 and self.choice2 == 2:
            gen_img(14)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 3 and self.choice2 == 0:
            gen_img(3)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 3 and self.choice2 == 1:
            gen_img(10)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 3 and self.choice2 == 2:
            gen_img(17)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 4 and self.choice2 == 0:
            gen_img(6)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 4 and self.choice2 == 1:
            gen_img(13)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 4 and self.choice2 == 2:
            gen_img(20)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 5 and self.choice2 == 0:
            gen_img(5)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 5 and self.choice2 == 1:
            gen_img(12)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 5 and self.choice2 == 2:
            gen_img(19)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 6 and self.choice2 == 0:
            gen_img(4)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 6 and self.choice2 == 1:
            gen_img(11)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)
        elif self.choice1 == 6 and self.choice2 == 2:
            gen_img(18)
            self.lab_pic.setPixmap(QPixmap('img.jpg'))
            self.lab_pic.setGeometry(10, 200, 600, 450)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window = AnotherWindow()

        ww = QWidget()

        lab_inst = QLabel(ww)
        lab_inst.setText("INSTRUCTIONS")
        lab_inst.move(40, 60)
        lab_inst.setFont(QFont('Arial', 30))

        lab_big1 = QLabel(ww)
        desc0 = "\nThere are 21 different types of highway images"
        desc0 += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        desc0 += " *Select the input conditions required from the two categories and click on the generate button to generate image"
        lab_big1.setText(desc0)
        lab_big1.setAlignment(QtCore.Qt.AlignLeft)
        lab_big1.setGeometry(30, 120, 1450, 660)
        lab_big1.setStyleSheet("border: 10px solid black;")
        lab_big1.setFont(QFont('Arial', 18))

        lab_small1 = QLabel(ww)
        lab_small1.setText("Directions & Bearings of Road:")
        lab_small1.setAlignment(QtCore.Qt.AlignLeft)
        lab_small1.setGeometry(50, 220, 780, 450)
        lab_small1.setStyleSheet("border: 5px solid black;")
        lab_small1.setFont(QFont('Arial', 20))

        lab_small1_txt = QLabel(ww)
        desc1 = "1. >N80e-3°W\n2. N50e-3°W to N79e-3°W\n3. N30e-3°W to N49e-3°W\n"
        desc1 += "\n4. 0°\n"
        desc1 += "\n5. >N80e-3°E\n6.N50e-3°E to N79e-3°E\n7.N30e-3°E to N49e-3°E"
        lab_small1_txt.setText(desc1)
        lab_small1_txt.setAlignment(QtCore.Qt.AlignLeft)
        lab_small1_txt.setGeometry(60, 290, 700, 450)
        lab_small1_txt.setFont(QFont('Arial', 20))

        lab_small1_exp = QLabel(ww)
        desc2 = "Where:\n\n*Direction and bearings of road\nat 100m ahead from middle of\nthe lane\n"
        desc2 += "\n1-3\nHighway road is curved to the left\n"
        desc2 += "\n4\nHighway road is straight\n"
        desc2 += "\n5-7\nHighway road is curved to the right"
        lab_small1_exp.setText(desc2)
        lab_small1_exp.setAlignment(QtCore.Qt.AlignCenter)
        lab_small1_exp.setGeometry(470, 240, 330, 400)
        lab_small1_exp.setFont(QFont('Arial', 15))
        lab_small1_exp.setStyleSheet("border: 1px solid black;")

        lab_small2 = QLabel(ww)
        desc3 = "\n\n Ego-car position:\n\n 1. Body of the car is slightly out of lane (left)"
        desc3 += "\n\n 2. Body of the car is in lane (middle)"
        desc3 += "\n\n 3. Body of the car is slightly out of lane (right)"
        lab_small2.setText(desc3)
        lab_small2.setAlignment(QtCore.Qt.AlignLeft)
        lab_small2.setGeometry(840, 220, 620, 450)
        lab_small2.setFont(QFont('Arial', 20))
        lab_small2.setStyleSheet("border: 5px solid black;")

        btn = QPushButton(ww)
        btn.setText('Click here to start the generator')
        btn.setFont(QFont('Arial', 20))
        btn.setGeometry(30, 20, 650, 50)
        btn.setStyleSheet("background-color: black; color: white")
        btn.move(820, 55)
        btn.clicked.connect(self.toggle_window)

        self.setCentralWidget(ww)

    def toggle_window(self, checked):
        if self.window.isVisible():
            self.window.hide()

        else:
            self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("Conditioned Highway Image Generator")
    w.resize(1500, 800)
    w.show()
    app.exec()

