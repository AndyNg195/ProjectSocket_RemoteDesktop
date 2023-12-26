import socket
from os import getlogin
from PIL import Image, ImageGrab #Import thư viện ImageGrab từ Pillow để chụp ảnh màn hình.

import io
from io import BytesIO
import numpy as np
from random import randint
import pyautogui
from threading import Thread
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt, QThread, pyqtSignal


print("[SERVER]: STARTED")
server_address = ('127.0.0.1', 12345)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address) # Server
sock.listen(5)
conn, addr = sock.accept()

# Deskop Show
class Dekstop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def ChangeImage(self):
        try:
            while True:
                img = ImageGrab.grab()
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                conn.send(img_bytes.getvalue())
                print('1')
            client_socket.close()
        except:
            print("DISCONNECTED")
        

    def Mouse_solving(self, mouse_data):
        if mouse_data.startswith("on_move"):
            _, x, y = mouse_data.split(',')
            pyautogui.moveTo(x, y)
        elif mouse_data.startswith("on_click"):
            _, x, y = mouse_data.split(',')
            pyautogui.click(x, y)
        elif mouse_data.startswith("on_scroll"):
            _, x, y, dx, dy = mouse_data.split(',')
            pyautogui.scroll(dx, dy)

    def Character_solving(self, char_data):
        print(0)


    
    def input_from_deviece(self):
        try:
            print("[SERVER]: CONNECTED: {0}!".format(addr[0]))
            while(True):
                data_nhận = conn.recv(9999999)
                data = data_nhận.decode('utf-8')
                if data.startswith("keyboard"):
                    key, char_data = data.split(',')
                    self.Character_solving(char_data)

                elif data.startswith("mouse"):
                    key, mouse_data = data.split(',')
                    self.Mouse_solving(mouse_data)
               
     
        except ConnectionResetError:
            QMessageBox.about(self, "ERROR", "[SERVER]: The remote host forcibly terminated the existing connection!")
            conn.close()
            


    def initUI(self):
        # Luồng nhận data
        self.input_thread = Thread(target = self.input_from_deviece, daemon = True)
        self.input_thread.start()
        # Luông gửi data 
        self.output_thread = Thread(target = self.ChangeImage, daemon = True)
        self.output_thread.start()
    
if _name_ == '_main_':
    
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
    

