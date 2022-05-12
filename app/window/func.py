import psutil
import win32con
import win32gui
import win32process
import win32ui
from ctypes import windll
from PIL import Image
import numpy as np
import cv2
import time
import autoit
import random
import bezier


def kill_awe():
    """Убить неизвестный процесс игры"""
    awe = 'AwesomiumProcess.exe'
    for bug in psutil.process_iter():
        if bug.name() == awe:
            bug.kill()


def get_hwnd(process_name: str):
    """Получить hwnd всех окон процесса"""
    array = []
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            def callback(hwnd, _):
                if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == proc.pid:
                        if hwnd not in array:
                            array.append(hwnd)
                return True

            win32gui.EnumWindows(callback, array)
    return array


def get_screenshot(hwnd):
    """Получить скриншот окна без фокуса по hwnd"""
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bit_map = win32ui.CreateBitmap()
    save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(save_bit_map)
    save_dc.BitBlt((0, 0), (w, h), mfc_dc, (0, 0), win32con.SRCCOPY)
    windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)
    bmp_info = save_bit_map.GetInfo()
    bmp_str = save_bit_map.GetBitmapBits(True)
    screenshot = Image.frombuffer('RGB', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_str, 'raw', 'BGRX', 0, 1)
    win32gui.DeleteObject(save_bit_map.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    return screenshot, left, top, right, bot


def compare(screen, template, thresh):
    """Сравнение изображений"""
    screen = np.float32(screen)
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, np.float32(template), cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= thresh)
    total = np.count_nonzero(loc)
    return total, loc


def focus_windows(hwnd):
    """Сфокусироваться на окне игры"""
    from datetime import datetime
    start_time = datetime.now()
    autoit.win_activate_by_handle(hwnd)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    return True


def mouse_move(x, y):
    """Движение мыши"""
    autoit.mouse_move(x, y, -3)
    return True


def click1(x, y):
    """Очеловеченный клик"""
    move = mouse_move(x, y)
    if move:
        autoit.mouse_down()
        time.sleep(random.uniform(0.0623, 0.1149))
        autoit.mouse_up()
        return True

def click():
    """Очеловеченный клик"""
    autoit.mouse_down()
    time.sleep(random.uniform(0.0623, 0.1149))
    autoit.mouse_up()


def move_to_center(le, to, ri, bo):
    """Движение мыши в центр экрана"""
    w = ri - le
    h = bo - to
    bezier_movements(int(le + w / 2), int(to + h / 2))


def move_to_random_center(le, to, ri, bo):
    """Движение мыши в неопределенное место в центре экрана"""
    w = ri - le
    h = bo - to
    bezier_movements(int(le + w / 2 + random.randint(-155, 155)), int(to + h / 2 + random.randint(-89, 189)))


def bezier_movements(*args, timeout=random.uniform(.0, 8.0)):
    """Нелинейное движение мыши"""
    speed = random.randint(40, 90)
    amount_of_points = random.randint(1, 5)
    control_points = []

    start = autoit.mouse_get_pos()  # Стартовая точка
    control_points.append(start)
    for i in range(amount_of_points):
        control_points.append((start[0] + random.randint(-20, 20), start[1] + random.randint(-20, 20)))

    if len(args) == 0:
        end = start[0] + random.randint(-300, 300), start[1] + random.randint(-300, 300)  # Конечная точка
        control_points.append(end)
    else:
        control_points.append(args)

    control_points = np.array(control_points)
    points = np.array([control_points[:, 0], control_points[:, 1]])
    degree = amount_of_points + 1
    curve = bezier.Curve(points, degree)
    curve_steps = speed
    for i in range(1, curve_steps + 1):
        x, y = curve.evaluate(i / curve_steps)
        autoit.mouse_move(int(x), int(y), 1)


def drag_cam(le, to, ri, bo):
    """Поворот камеры на ~90 градусов"""
    move_to_center(le, to, ri, bo)
    pix = [-18, 18]
    rand = random.randint(0, 1)
    pos = autoit.mouse_get_pos()
    autoit.mouse_click_drag(x1=pos[0], y1=pos[1], x2=pos[0] + pix[rand], y2=pos[1] + 5, button="right", speed=25)
