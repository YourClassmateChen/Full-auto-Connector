from decimal import Decimal
from pynput.mouse import Events  # 遍历输入
from pynput.keyboard import Key, Controller as KeyboardCtrl  # 输出>>键盘
from pynput.mouse import Button, Controller as MouseCtrl  # 输入<<鼠标
from time import sleep  # 等待(射击间隔)
from threading import Event, Thread  # 多线程
from easygui import buttonbox
from sys import exit as ex
from easygui import enterbox

sleep_time = 0.0120  # 缺省值
exit_value = False

time_dict = {}
gun_list = []
with open('def_file.txt', 'r', encoding='utf-8') as f:
    time_list = f.read().splitlines()
    for i in time_list:
        time_dict[i.split('=')[0]] = i.split('=')[1]
    for i in time_dict:
        gun_list.append(i)


def run() -> None:  # 连点线程
    thevent.clear()  # 开启连点事件
    while True:
        if thevent.is_set():  # 检查连点事件
            break
        pan.press(Key.left)  # 按下
        pan.release(Key.left)  # 松开
        # sleep(0.01428)  # 等待射击间隔-Type63
        # sleep(0.0165)  # 等待射击间隔-SKS
        # sleep(0.0120)  # 等待设计间隔-M1 Garand
        sleep(sleep_time)


kb = MouseCtrl()  # 鼠标控制对象
pan = KeyboardCtrl()  # 键盘控制对象
thevent = Event()


def main_win():
    global sleep_time
    global exit_value
    while True:
        button_input = buttonbox('-呈阶梯状分布-\n全自动连点器', 'test', gun_list)
        if button_input is None:
            exit_value = True
            return SystemExit
        for i in gun_list:
            if button_input == i:
                sleep_time = float(Decimal(time_dict[i]))
                print(sleep_time)
                break


main_window = Thread(target=main_win)
main_window.start()
# input("回车开始,输入v即可退出")

with Events() as event:
    for i in event:
        if exit_value:
            ex()
        if isinstance(i, Events.Click) and i.button == Button.left:
            if i.pressed:
                fire = Thread(target=run)
                fire.start()
            else:
                thevent.set()
