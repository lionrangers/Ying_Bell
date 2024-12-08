import tkinter as tk
from tkinter import Button
from picamera2 import Picamera2
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
from threading import Thread
import time

# GPIO定义
LED_GPIO = 27
ENABLE_GPIO = 4
BUTTON_GPIO = 17

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(ENABLE_GPIO, GPIO.OUT)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(ENABLE_GPIO, GPIO.HIGH)
GPIO.output(LED_GPIO, GPIO.HIGH)

# 摄像头初始化
camera = Picamera2()

# 全局变量
camera_running = False
root = None
canvas = None
screen_width = 0
screen_height = 0
exit_flag = False  # 全局退出标志

def start_camera():
    """
    启动摄像头并动态调整分辨率
    """
    global camera_running
    if not camera_running:
        print("Initializing Camera...")
        camera.configure(camera.create_preview_configuration(main={"size": (screen_width - 300, screen_height)}))
        camera.start()
        camera_running = True
        print("Camera started!")
        update_frame()

def stop_camera():
    """
    停止摄像头
    """
    global camera_running
    if camera_running:
        camera.stop()
        camera_running = False
        print("Camera stopped!")

def update_frame():
    """
    在 Tkinter 窗口中实时更新摄像头画面
    """
    if camera_running:
        frame = camera.capture_array()
        frame_image = Image.fromarray(frame)
        frame_photo = ImageTk.PhotoImage(frame_image)

        canvas.create_image(0, 0, anchor=tk.NW, image=frame_photo)
        canvas.image = frame_photo

        root.after(10, update_frame)

def monitor_button():
    """
    监控物理按键，用于启动摄像头
    """
    global exit_flag
    while not exit_flag:
        if GPIO.input(BUTTON_GPIO) == GPIO.HIGH:
            print("Button Pressed!")
            start_camera()
            time.sleep(0.5)  # 防止重复触发
        time.sleep(0.1)

def exit_program():
    """
    关闭窗口并退出程序
    """
    global exit_flag, root
    exit_flag = True  # 设置退出标志
    stop_camera()  # 停止摄像头
    GPIO.output(LED_GPIO, GPIO.LOW)
    GPIO.output(ENABLE_GPIO, GPIO.LOW)
    GPIO.cleanup()  # 清理 GPIO 资源
    print("Exiting program...")
    root.destroy()  # 关闭 Tkinter 窗口

def create_gui():
    """
    创建 Tkinter 图形界面
    """
    global root, canvas, screen_width, screen_height
    root = tk.Tk()
    root.title("Camera Viewer")
    root.attributes('-fullscreen', True)  # 自动全屏

    # 获取屏幕分辨率
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(f"Screen resolution: {screen_width}x{screen_height}")

    # 创建画布，用于显示摄像头画面
    canvas_width = screen_width - 300  # 右侧留出 300px 放按钮
    canvas_height = screen_height
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
    canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # 添加按钮框架
    button_frame = tk.Frame(root, bg="gray")  # 背景颜色用于调试布局
    button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

    # 添加按钮：停止摄像头
    stop_button = Button(button_frame, text="Stop Camera", command=stop_camera, height=2, width=15)
    stop_button.pack(pady=20)

    # 添加按钮：退出程序
    exit_button = Button(button_frame, text="Exit Program", command=exit_program, height=2, width=15)
    exit_button.pack(pady=20)

    # 配置行列权重，让画布和按钮适应全屏
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # 绑定 Esc 键退出全屏模式
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))

    root.mainloop()


if __name__ == "__main__":
    try:
        button_thread = Thread(target=monitor_button, daemon=True)
        button_thread.start()

        create_gui()
    finally:
        GPIO.output(LED_GPIO, GPIO.LOW)
        GPIO.output(ENABLE_GPIO, GPIO.LOW)
        GPIO.cleanup()

