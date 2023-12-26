# Socket
import socket

import pickle# thư viện dùng để nén dữ liệu 

from pynput import mouse

server_address = ('localhost', 9091)



# Work with Image
from PIL import ImageGrab #Import thư viện ImageGrab từ Pillow để chụp ảnh màn hình.
import io #Import thư viện io để thao tác với dữ liệu nhị phân.
import numpy as np #Import thư viện numpy để làm việc với mảng nhiều chiều.
from random import randint #Import hàm randint để tạo số ngẫu nhiên.
import pyautogui #Import thư viện pyautogui để làm việc với điều khiển màn hình.

# Thread
import threading

from threading import Thread #Import class Thread để tạo và quản lý các thread.

# PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt
# from PyQt5.QtWidgets import ...: Import các lớp và phương thức từ PyQt5 để xây dựng giao diện người dùng.
#from PyQt5.QtGui import ...: Import các lớp và phương thức từ PyQt5 để làm việc với đồ họa.
#from PyQt5.QtCore import ...: Import các lớp và phương thức từ PyQt5 để sử dụng các tính năng cơ bản của PyQt5.

from pynput import keyboard# thư viện để nhập kí tự từ bàn phím
from datetime import datetime #datetime: Thư viện datetime dùng để làm việc với thời gian.

class Dekstop(QMainWindow):
    def __init__(self):#def __init__(self):: Hàm khởi tạo của class Dekstop.
        super().__init__()
        self.initUI()


    def initUI(self):#def initUI(self):: Hàm tạo giao diện người dùng của ứng dụng.
        self.pixmap = QPixmap() # hình nền được lấy từ server
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 400, 90))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("[CLIENT] Remote Desktop: " + str(randint(99999, 999999)))
        self.start = Thread(target=self.ChangeImage, daemon=True)

        self.btn = QPushButton(self) # nút khởi động chương trình
        self.btn.move(5, 55)
        self.btn.resize(390, 30)
        self.btn.setText("Start Demo")
        self.btn.clicked.connect(self.StartThread)

        self.exit_btn = QPushButton(self)  # Thêm nút thoát
        self.exit_btn.move(305, 5)
        self.exit_btn.resize(90, 20)
        self.exit_btn.setText("Exit")
        self.exit_btn.clicked.connect(self.ExitApp)  # Kết nối nút thoát với hàm ExitApp
    
        self.ip = QLineEdit(self) 
        self.ip.move(5, 5)
        self.ip.resize(390, 20)
        self.ip.setPlaceholderText("IP")

        self.port = QLineEdit(self)
        self.port.move(5, 30)
        self.port.resize(390, 20)
        self.port.setPlaceholderText("PORT")

    def StartThread(self):#def StartThread(self):: Hàm khởi động thread khi nút "Start Demo" được nhấn.

        self.start.start()
        Thread1.start()
        Thread2.start()
    
    
    
    def ExitApp(self):
        # Dừng các thread và giải phóng tài nguyên trước khi thoát ứng dụng ...
        Thread1.join()
        Thread2.join() 
        self.close()

    def ChangeImage(self):#def ChangeImage(self):: Hàm chụp ảnh màn hình và gửi nó tới máy chủ thông qua kết nối socket.
        try:
            if len(self.ip.text()) != 0 and len(self.port.text()):
                sock = socket.socket()
                sock.connect((self.ip.text(), int(self.port.text())))
                while True:
                    img = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    sock.send(img_bytes.getvalue())
                sock.close()
        except:
            print("DISCONNECTED")

# //////////////////////////////////////                     0000000000000000000000000000000            ////////////////////////////////// 
            
# Nhiệm vụ hiện tại là phân luồng và gửi thông tin từ client sang server


logdata = []
def getKeyName(key):#Hàm này trả về tên của phím dựa trên kiểu của phím (KeyCode hoặc không phải).
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)
    

def keyPressed(key):#Hàm này được gọi khi một phím được nhấn. Nó lấy tên của phím và thêm thông tin về sự kiện vào danh sách logdata cùng với thời gian nhấn phím.
   
    keyName = getKeyName(key)
    logdata.append([datetime.now().timestamp(), keyName])


def keyReleased(key,logdata):
    if key == keyboard.Key.esc:
        print(logdata)
        send_keyboard_data(logdata)
        return False

def send_keyboard_data(logdata):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)  
    message=f"{keyboard},{logdata}"
    client_socket.send(message.encode('utf-8'))
    client_socket.close()




def putkeyboard(logdata):
    with keyboard.Listener(#Sử dụng keyboard.Listener để theo dõi sự kiện nhấn và nhả phím.
        on_press=keyPressed,#Thực hiện hàm keyPressed khi một phím được nhấn.
        on_release=keyReleased) as listener:
        listener.join()
   
        
Thread1=threading.Thread(target=putkeyboard,args=(logdata,))

#  ///////////////                               ooooooooooooooooooo              /////////////////////////////



def on_move(x, y):
    logdata2 = []
    logdata2.append([datetime.now().timestamp(), f'Mouse moved to ({x}, {y})'])
    send_keymouse_data(logdata2,"on_move")
     #mouse thì sẽ gửi là message = {key}, {trường hợp}, {x}, {y} nếu th là on_scroll thì thêm {dx}, {dy} cuối nũa
    

def on_click(x, y, button, pressed):
    logdata2 = []
    action = 'Pressed' if pressed else 'Released'
    logdata2.append([datetime.now().timestamp(), f'Mouse {action} at ({x}, {y}) with {button}'])
    send_keymouse_data(logdata2,"on_click")
    if (x,y) ==(305,5)& pressed:
         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         client_socket.connect(server_address)
         data="disconnect...."
         message=f"{exit},{data}"
         client_socket.send(message.encode('utf-8'))
         client_socket.close()



def on_scroll(x, y, dx, dy):
    logdata2 = []
    logdata2.append([datetime.now().timestamp(), f'Scrolled at ({x}, {y}) with delta ({dx}, {dy})'])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    th="on_roll"
    message=f"{mouse},{th},{logdata2}{dx}{dy}"
    client_socket.send(message.encode('utf-8'))
    client_socket.close()
#on_move: Được gọi khi chuột di chuyển.
#on_click: Được gọi khi một nút chuột được nhấn hoặc nhả.
#on_scroll: Được gọi khi chuột được cuộn.
# Lắng nghe sự kiện chuột

def send_keymouse_data(data,th):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
     # Tạo chuỗi message sử dụng f-string
    message = f"{mouse},{th},{data}"
        # Gửi message thông qua socket sau khi mã hóa bằng UTF-8
    client_socket.send(message.encode('utf-8'))
    client_socket.close()


def putkeymouse():
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
        listener.join()
    
Thread2=threading.Thread(target=putkeymouse)


# ///////////////////////////////            0000000000000000000000000000       ///////////////////////////////// 



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
    
   # app = QApplication(sys.argv): Khởi tạo ứng dụng PyQt.
#ex = Dekstop(): Tạo một đối tượng của class Dekstop.
#ex.show(): Hiển thị cửa sổ ứng dụng.
#sys.exit(app.exec()): Chạy vòng lặp sự kiện của PyQt.
    # Ghi rõ các kiểu dữ liệu khi truyền sang server