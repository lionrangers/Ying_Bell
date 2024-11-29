import tkinter as tk
from tkinter import Button
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time
from threading import Thread

# GPIO引脚定义
LED_GPIO = 27        # 按键LED控制引脚
ENABLE_GPIO = 4      # 按键使能引脚
BUTTON_GPIO = 17     # 按键触发引脚

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO, GPIO.OUT)        # 配置LED为输出
GPIO.setup(ENABLE_GPIO, GPIO.OUT)    # 配置使能为输出
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 配置按键为输入

# 打开按键功能和点亮LED
GPIO.output(ENABLE_GPIO, GPIO.HIGH)  # 启用按键功能
GPIO.output(LED_GPIO, GPIO.HIGH)     # 点亮按键LED

# 初始化摄像头
camera = Picamera2()

# 摄像头控制逻辑
def start_camera():
    camera.configure(camera.create_preview_configuration())
    camera.start()
    print("Camera started!")

def stop_camera():
    camera.stop()
    print("Camera stopped!")

# 按键监控逻辑
def monitor_button():
    while True:
        if GPIO.input(BUTTON_GPIO) == GPIO.HIGH:  # 检测到按键按下
            start_camera()
            time.sleep(0.5)  # 按键去抖
        time.sleep(0.1)

# 创建屏幕控制界面
def create_gui():
    root = tk.Tk()
    root.title("Camera Control")
    root.geometry("400x200")

    # 屏幕上的“关闭摄像头”按钮
    stop_btn = Button(root, text="Stop Camera", command=stop_camera)
    stop_btn.pack(pady=50)

    root.mainloop()

# 主程序入口
if __name__ == "__main__":
    try:
        # 启动按键监控线程
        button_thread = Thread(target=monitor_button, daemon=True)
        button_thread.start()

        # 启动屏幕控制界面
        create_gui()

    finally:
        # 程序退出时关闭LED并释放资源
        GPIO.output(LED_GPIO, GPIO.LOW)     # 关闭LED
        GPIO.output(ENABLE_GPIO, GPIO.LOW) # 禁用按键功能
        GPIO.cleanup()
