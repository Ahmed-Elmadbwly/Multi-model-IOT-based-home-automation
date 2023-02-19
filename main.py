# بسم الله الرحمن الرحيم والصلاه والسلام علي افضل المرسلين
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import serial
import re
db = sqlite3.connect('Data.db')
cr = db.cursor()
cr.execute("Create table if not exists user(name text, email text, password text)")
task_cr = db.cursor()


class WelcomePage(QWidget):
    def __init__(self):
        super(WelcomePage, self).__init__()

        with open('css/welcome.css') as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setWindowTitle('Productivity Club')
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(50, 0, 50, 50)

        welcome_text = QLabel("Welcome To")
        welcome_text.setObjectName('wel')

        txt2 = QLabel("Multi model IOT based home\n automation ")
        txt2.setObjectName("txt2")

        welcome_text.setAlignment(Qt.AlignCenter)
        txt2.setAlignment(Qt.AlignCenter)

        login_button = QPushButton("Login")
        login_button.setObjectName("login")

        main_layout.addWidget(welcome_text)
        main_layout.addWidget(txt2)
        main_layout.addWidget(login_button)

        def go_to_login():
            Windows.setCurrentIndex(1)

        login_button.clicked.connect(go_to_login)

        self.setLayout(main_layout)

class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        with open("css/login.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        lb1 = QLabel("Login")
        lb1.setObjectName("lb1")
        lb2 = QLabel("Enter Your Email And Password")
        lb2.setObjectName("lb2")

        lb1.setAlignment(Qt.AlignCenter)
        lb2.setAlignment(Qt.AlignCenter)

        email_field = QLineEdit()
        email_field.setPlaceholderText("Email")
        email_field.setObjectName("field")

        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)
        password_field.setPlaceholderText("Password")
        password_field.setObjectName("field")

        login_btn = QPushButton("Login")
        login_btn.setObjectName("login")


        main_layout.addWidget(lb1)
        main_layout.addWidget(lb2)
        main_layout.addWidget(email_field)
        main_layout.addWidget(password_field)
        main_layout.addWidget(login_btn)
        main_layout.insertSpacing(1, 50)
        main_layout.insertSpacing(2, 10)

        def go_back():
            Windows.setCurrentIndex(0)

        def check_input():
            cr.execute(f"select name , email , password from user "
                       f"where email='{email_field.text()}' and password='{password_field.text()}'")
            result = cr.fetchall()
            if email_field.text() == "" or password_field == "":
                QMessageBox.warning(self, "warning", "You can't leave any input field empty", QMessageBox.Ok)
            elif len(result) >= 1:
                # SET USER DATA
                home_page = Home(result[0][0], email_field.text(), password_field.text())
                Windows.addWidget(home_page)  # 8
                Windows.setCurrentIndex(Windows.count() - 1)
            else:
                QMessageBox.warning(self, "warning", "Email and Password are incorrect", QMessageBox.Ok)

        back.clicked.connect(go_back)
        login_btn.clicked.connect(check_input)
        self.setLayout(main_layout)


class Btn(QPushButton):
    def __init__(self, path):
        super().__init__()
        self.setIcon(QIcon(path))
        self.setIconSize(QSize(150, 150))
        with open("css/btn.css") as file:
            style = file.read()
            self.setStyleSheet(style)

class btn(QPushButton):
    def __init__(self, path):
        super().__init__()
        self.setIcon(QIcon(path))
        self.setIconSize(QSize(50, 50))
        with open("css/btn.css") as file:
            style = file.read()
            self.setStyleSheet(style)

class Home(QWidget):
    def __init__(self, user_name, email, password):
        super().__init__()

        with open("css/home.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 30)

        home_icon = QPushButton()
        home_icon.setIcon(QIcon("Icons/home.png"))
        home_icon.setIconSize(QSize(40, 40))

        txt1 = QLabel("Name : " + user_name)
        txt1.setObjectName("name")
        change_name = QPushButton()
        change_name.setIcon(QIcon("Icons/pencil.png"))
        change_name.setIconSize(QSize(20, 20))
        change_name.setFixedSize(35, 35)
        change_name.setObjectName("pen")

        def c_name():
            text, ok = QInputDialog().getText(self, "Change Your Name", "User name:", QLineEdit.Normal)
            if ok:
                cr.execute(f"update user set name='{text}' where email='{email}' and password='{password}'")
                db.commit()
                txt1.setText("Name : " + text)

        change_name.clicked.connect(c_name)

        name_lay = QHBoxLayout()
        name_lay.addWidget(txt1)
        name_lay.addWidget(change_name)

        txt2 = QLabel("Email : " + email)
        txt2.setObjectName("name")
        change_email = QPushButton()
        change_email.setIcon(QIcon("Icons/pencil.png"))
        change_email.setIconSize(QSize(20, 20))
        change_email.setFixedSize(35, 35)
        change_email.setObjectName("pen")

        def c_email():
            text, ok = QInputDialog().getText(self, "Change Your Email", "Email :", QLineEdit.Normal)
            if ok:
                reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                is_email = re.fullmatch(reg, text)
                if is_email:
                    cr.execute("select email from user")
                    emails = cr.fetchall()
                    if (text,) in emails:
                        QMessageBox.warning(self, "warning", "This Email is already used, Please use another one",
                                            QMessageBox.Ok)
                    else:
                        cr.execute(f"update user set email='{text}' where email='{email}' and password='{password}'")
                        db.commit()
                        txt2.setText("Email : " + text)
                else:
                    QMessageBox.warning(self, "warning", "Please enter a valid email \nSuch as : Mostafa_12@gmail.com ",
                                        QMessageBox.Ok)

        change_email.clicked.connect(c_email)

        email_lay = QHBoxLayout()
        email_lay.addWidget(txt2)
        email_lay.addWidget(change_email)

        txt3 = QLabel("Password : " + len(password) * "*")
        txt3.setObjectName("name")
        change_pass = QPushButton()
        change_pass.setIcon(QIcon("Icons/pencil.png"))
        change_pass.setIconSize(QSize(20, 20))
        change_pass.setFixedSize(35, 35)
        change_pass.setObjectName("pen")

        def c_pass():
            text, ok = QInputDialog().getText(self, "Change Your Name", "User name:", QLineEdit.Normal)
            if ok:
                cr.execute(f"update user set password='{text}' where email='{email}' ")
                db.commit()
                txt3.setText("Password : " + len(text) * "*")
                password = text

        change_pass.clicked.connect(c_pass)

        pass_lay = QHBoxLayout()
        pass_lay.addWidget(txt3)
        pass_lay.addWidget(change_pass)

        txt4 = QLabel("Our Features")
        txt4.setObjectName("title")

        to_into=Btn("Icons/domotics.png")
        to_ex=Btn("Icons/logout.png")

        btn_lay = QHBoxLayout()
        btn_lay.addWidget(to_into)
        btn_lay.addWidget(to_ex)

        def exit():
            sys.exit(app.exec_())

        def go_to_Work():
            Windows.setCurrentIndex(2)

        to_ex.clicked.connect(exit)
        to_into.clicked.connect(go_to_Work)


        txt4.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(home_icon)
        main_layout.addLayout(name_lay)
        main_layout.addLayout(email_lay)
        main_layout.addLayout(pass_lay)
        main_layout.addWidget(txt4)
        main_layout.addLayout(btn_lay)
        main_layout.setSpacing(20)
        main_layout.insertSpacing(4, 50)
        self.setLayout(main_layout)

class Work(QWidget):
    def __init__(self):
        super().__init__()

        with open("css/home.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        def go_back():
            Windows.setCurrentIndex(3)
        back.clicked.connect(go_back)

        hl1 = QHBoxLayout()
        hl2 = QHBoxLayout()
        hl3 = QHBoxLayout()
        hl4 = QHBoxLayout()
        hl5 = QHBoxLayout()

        vl1 = QVBoxLayout()
        vl2 = QVBoxLayout()
        vl3 = QVBoxLayout()
        vl4 = QVBoxLayout()
        vl5 = QVBoxLayout()
        vl6 = QVBoxLayout()
        vl7 = QVBoxLayout()
        vl8 = QVBoxLayout()
        vl9 = QVBoxLayout()
        vl10 = QVBoxLayout()

        room1=btn("Icons/biometrics.png")
        l_room1=QLabel("room 1")
        l_room1.setObjectName("IconLabel")
        l_room1.setAlignment(Qt.AlignCenter)
        vl1.addWidget(room1)
        vl1.addWidget(l_room1)

        room2 = btn("Icons/biometrics.png")
        l_room2 = QLabel("room 2")
        l_room2.setObjectName("IconLabel")
        l_room2.setAlignment(Qt.AlignCenter)
        vl2.addWidget(room2)
        vl2.addWidget(l_room2)

        room3 = btn("Icons/biometrics.png")
        l_room3 = QLabel("room 3")
        l_room3.setObjectName("IconLabel")
        l_room3.setAlignment(Qt.AlignCenter)
        vl3.addWidget(room3)
        vl3.addWidget(l_room3)

        room4 = btn("Icons/biometrics.png")
        l_room4 = QLabel("room 4")
        l_room4.setObjectName("IconLabel")
        l_room4.setAlignment(Qt.AlignCenter)
        vl4.addWidget(room4)
        vl4.addWidget(l_room4)

        room5 = btn("Icons/biometrics.png")
        l_room5 = QLabel("room 5")
        l_room5.setObjectName("IconLabel")
        l_room5.setAlignment(Qt.AlignCenter)
        vl5.addWidget(room5)
        vl5.addWidget(l_room5)

        room6 = btn("Icons/biometrics.png")
        l_room6 = QLabel("room 6")
        l_room6.setObjectName("IconLabel")
        l_room6.setAlignment(Qt.AlignCenter)
        vl6.addWidget(room6)
        vl6.addWidget(l_room6)

        room7 = btn("Icons/biometrics.png")
        l_room7 = QLabel("room 7")
        l_room7.setObjectName("IconLabel")
        l_room7.setAlignment(Qt.AlignCenter)
        vl7.addWidget(room7)
        vl7.addWidget(l_room7)

        room8 = btn("Icons/biometrics.png")
        l_room8 = QLabel("room 8")
        l_room8.setObjectName("IconLabel")
        l_room8.setAlignment(Qt.AlignCenter)
        vl8.addWidget(room8)
        vl8.addWidget(l_room8)


        room9 = btn("Icons/biometrics.png")
        l_room9 = QLabel("All on")
        l_room9.setObjectName("IconLabel")
        l_room9.setAlignment(Qt.AlignCenter)
        vl9.addWidget(room9)
        vl9.addWidget(l_room9)

        room10 = btn("Icons/biometrics.png")
        l_room10 = QLabel("All off")
        l_room10.setObjectName("IconLabel")
        l_room10.setAlignment(Qt.AlignCenter)
        vl10.addWidget(room10)
        vl10.addWidget(l_room10)

        hl1.addLayout(vl1)
        hl1.addLayout(vl2)
        hl2.addLayout(vl3)
        hl2.addLayout(vl4)
        hl3.addLayout(vl5)
        hl3.addLayout(vl6)
        hl4.addLayout(vl7)
        hl4.addLayout(vl8)
        hl5.addLayout(vl9)
        hl5.addLayout(vl10)

        btn_lay=QVBoxLayout()
        btn_lay.setContentsMargins(30, 40, 40, 30)
        btn_lay.addLayout(hl1)
        btn_lay.addLayout(hl2)
        btn_lay.addLayout(hl3)
        btn_lay.addLayout(hl4)
        btn_lay.addLayout(hl5)

        ser=serial.Serial("COM5",baudrate=9600,timeout=1)

        def room_1():
            ser.write(b'a')

        def room_2():
            ser.write(b'b')

        def room_3():
           ser.write(b'c')

        def room_4():
           ser.write(b'd')

        def room_5():
           ser.write(b'e')

        def room_6():
           ser.write(b'f')

        def room_7():
           ser.write(b'g')

        def room_8():
           ser.write(b'h')

        def allon():
            ser.write(b'y')

        def alloff():
            ser.write(b'z')

        room1.clicked.connect(room_1)
        room2.clicked.connect(room_2)
        room3.clicked.connect(room_3)
        room4.clicked.connect(room_4)
        room5.clicked.connect(room_5)
        room6.clicked.connect(room_6)
        room7.clicked.connect(room_7)
        room8.clicked.connect(room_8)
        room9.clicked.connect(allon)
        room10.clicked.connect(alloff)

        self.setLayout(btn_lay)






app = QApplication(sys.argv)
Windows = QStackedWidget()
Windows.setGeometry(500, 100, 400, 600)
Windows.setStyleSheet('background-color: #1e4f65')
Windows.addWidget(WelcomePage())  # 0
Windows.addWidget(LoginPage())  # 1
Windows.addWidget(Work()) #2
Windows.show()
sys.exit(app.exec_())
