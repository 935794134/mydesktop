import json
import sys
import ctypes
from ctypes import wintypes
from pathlib import Path
from PySide6.QtWidgets import QApplication,QWidget, QLabel, QGridLayout,QPushButton,QSystemTrayIcon,QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


#card--->桌面看的
#window--->管理card的窗口

path=Path(__file__).parent
path_json = path / "data.json"
path_ico = path / "icon.ico"

#Win32 的常量
HWND_BOTTOM = 1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010

#声明参数类型
#64 位下窗口句柄是 8 字节，不声明的话 ctypes 默认按 32 位整数传，句柄会被截断
user32 = ctypes.WinDLL("user32", use_last_error=True)
user32.SetWindowPos.argtypes = [
    wintypes.HWND,
    wintypes.HWND,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint,
]
user32.SetWindowPos.restype = wintypes.BOOL

main_process = QApplication(sys.argv)

screen_height = main_process.primaryScreen().size().height()
screen_width = main_process.primaryScreen().size().width()

window_height = int(screen_height * 0.8)
window_width = int(screen_width * 0.5)

main_window = QWidget()
main_window.setWindowTitle("My Desktop")
main_window.resize(window_width, window_height)

main_window_layout = QGridLayout(main_window)
main_window_layout.setContentsMargins(10, 10, 10, 10)

main_process.setQuitOnLastWindowClosed(False)

#创建后台托盘图标
back_icon = QSystemTrayIcon(main_window)
back_icon.setIcon(QIcon(str(path_ico)))
back_icon.setToolTip("My Desktop")

choicing_card_index = 1
def change_choice_card():
    global choicing_card_index
    choicing_card_index = ((choicing_card_index) % len(cards))+1
    choicing_card_change_button.setText(f"Choicing Card:{choicing_card_index}")

def card_go_up():
    global choicing_card_index
    write_card(choicing_card_index,"y",read_card_infor(choicing_card_index)["y"]-ratelist[rate_index])
    builded_cards[choicing_card_index-1].move(read_card_infor(choicing_card_index)["x"],read_card_infor(choicing_card_index)["y"])

def card_go_down():
    global choicing_card_index
    write_card(choicing_card_index,"y",read_card_infor(choicing_card_index)["y"]+ratelist[rate_index])
    builded_cards[choicing_card_index-1].move(read_card_infor(choicing_card_index)["x"],read_card_infor(choicing_card_index)["y"])

def card_go_left():
    global choicing_card_index
    write_card(choicing_card_index,"x",read_card_infor(choicing_card_index)["x"]-ratelist[rate_index])
    builded_cards[choicing_card_index-1].move(read_card_infor(choicing_card_index)["x"],read_card_infor(choicing_card_index)["y"])

def card_go_right():
    global choicing_card_index
    write_card(choicing_card_index,"x",read_card_infor(choicing_card_index)["x"]+ratelist[rate_index])
    builded_cards[choicing_card_index-1].move(read_card_infor(choicing_card_index)["x"],read_card_infor(choicing_card_index)["y"])

ratelist = [1, 5, 10, 20, 50]
rate_index = 0
def change_moving_rate():
    global rate_index
    rate_index = (rate_index + 1) % len(ratelist)
    rate_change_button.setText(f"Moving Rate:{ratelist[rate_index]}")

def change_card_title_visiable():
    now_sitting_to=not(read_sitting("title_visible"))
    write_sitting("title_visible",now_sitting_to)
    for card in builded_cards:
        card.findChild(QLabel, "card_title").setVisible(now_sitting_to)
    
#json读写
def read_full_data_json():
    with open(path_json, "r", encoding="utf-8") as f:
        full_data_json = json.load(f)
    return full_data_json

def read_sittings():
    return read_full_data_json()["sittings"]

def read_sitting(sittting_name):
    return read_sittings()[sittting_name]

def read_card_infor(card_index):
    full_data_json = read_full_data_json()
    for card in full_data_json["cards"]:
        if card["index"] == card_index:
            return card

def write_full_json(full_data_json):
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(full_data_json, f, ensure_ascii=False, indent=4)

def write_card(card_index,info_name,new_value):
    card=read_card_infor(card_index)
    card[info_name]=new_value
    full_data_json = read_full_data_json()
    full_data_json["cards"][card_index-1]=card
    write_full_json(full_data_json)

def write_sitting(sitting_name,value):
    sittings=read_sittings()
    sittings[sitting_name]=value
    full_data_json = read_full_data_json()
    full_data_json["sittings"]=sittings
    write_full_json(full_data_json)

#绘制card
def build_card(card_index):
    card_data = read_card_infor(card_index)
    card = QWidget()
    card.setObjectName("card")
    card.setWindowFlags(
            Qt.FramelessWindowHint          #去掉标题栏
            | Qt.Tool                       #不进任务栏
            | Qt.WindowStaysOnBottomHint    #请求置底
            | Qt.WindowTransparentForInput  #不吃鼠标
    )
    card.setAttribute(Qt.WA_TranslucentBackground)#背景
    
    card_layout = QGridLayout(card)
    card_layout.setContentsMargins(0, 0, 0, 0)#内部组件距离

    card_background = QWidget(card)
    card_background.setObjectName("card_background")
    background_color=read_sitting("background_rgb")+","+read_sitting("background_opacity")
    card_background.setStyleSheet(
        f"""
        #card_background {{
            background-color: rgba({background_color});
            border-radius: 10px;
        }}
        """
    )
    card_layout.addWidget(card_background)
    
    card_title = QLabel(card_data["title"],card_background)
    card_title.setObjectName("card_title")
    card_title.setStyleSheet("color:rgba(232, 234, 240, 0.55); background: transparent;")
    card_title.setVisible(read_sitting("title_visible"))

    card_info = QLabel(card_data["info"], card_background)
    card_info.setStyleSheet("color: #F5F6FA; background: transparent;")
    card_info.setWordWrap(True)

    card_inner_layout = QGridLayout(card_background)
    card_inner_layout.setContentsMargins(20, 16, 20, 16)
    card_inner_layout.setSpacing(6)
    card_inner_layout.addWidget(card_title, 0, 0)
    card_inner_layout.addWidget(card_info, 1, 0 )

    card.resize(card_data["width"], card_data["height"])
    card.move(card_data["x"], card_data["y"])

    return card

def to_buttom(card):
    hwnd = int(card.winId())
    user32.SetWindowPos(hwnd, HWND_BOTTOM, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)

def quit_back():
    back_icon.hide()
    main_process.quit()

#创建按钮
up_button = QPushButton("↑", main_window)
main_window_layout.addWidget(up_button,0,1)
up_button.clicked.connect(card_go_up)

down_button = QPushButton("↓", main_window)
main_window_layout.addWidget(down_button,2,1)
down_button.clicked.connect(card_go_down)

left_button = QPushButton("←", main_window)
main_window_layout.addWidget(left_button,1,0)
left_button.clicked.connect(card_go_left)

right_button = QPushButton("→", main_window)
main_window_layout.addWidget(right_button,1,2)
right_button.clicked.connect(card_go_right)

rate_change_button = QPushButton(f"Moving Rate:{ratelist[rate_index]}", main_window)
main_window_layout.addWidget(rate_change_button,1,1)
rate_change_button.clicked.connect(change_moving_rate)

choicing_card_change_button = QPushButton(f"Choicing Card:{choicing_card_index}", main_window)
main_window_layout.addWidget(choicing_card_change_button,2,2)
choicing_card_change_button.clicked.connect(change_choice_card)

#设置按钮
change_card_title_visiable_button = QPushButton("change card title visiable")
main_window_layout.addWidget(change_card_title_visiable_button,0,2)
change_card_title_visiable_button.clicked.connect(change_card_title_visiable)

main_window.show()

back_list=QMenu()
quit_action=back_list.addAction("退出")
back_icon.setContextMenu(back_list)
back_icon.show()
quit_action.triggered.connect(quit_back)

#桌面card的名称列表，用于记录有了哪些card
cards=[]
for card in read_full_data_json()["cards"]:
    cards.append(card["index"])

builded_cards=[]
for card_index in cards:
    card = build_card(card_index)
    card.show()
    to_buttom(card)
    builded_cards.append(card)

sys.exit(main_process.exec())