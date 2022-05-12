import time
from threading import Thread

import autoit
import cv2

from app.window.func import *

screenshot = Image.Image
left = int
top = int
right = int
bot = int
self_hp = int
target_hp = int


class Personage:
    def __init__(self):
        super(Personage, self).__init__()
        self.buttons = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        self.windows = get_hwnd('AsteriosGame.exe')
        self.system_buttons = ['HOME', 'ALT+L']

    def stream(self, hwnd):
        def _thread(handle):
            global screenshot, left, top, right, bot, target_hp, self_hp
            while True:
                screenshot, left, top, right, bot = get_screenshot(handle)
                temp_self_hp = self.get_self_hp()
                temp_target_hp = self.get_target_hp()
                if temp_self_hp is not None:
                    self_hp = temp_self_hp
                if temp_target_hp is not None:
                    target_hp = temp_target_hp

        Thread(target=_thread, args=(hwnd,), daemon=True).start()

    def get_self_hp(self):
        """Получить уровень хп персонажа"""
        sc = {}
        slc = {}
        cc = {}
        hp_min_max = ""
        nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"]
        template = cv2.imread('./../../templates/frames/self_bar.png', 0)
        frame_end = cv2.imread('./../../templates/frames/frame_end.png', 0)
        slash = cv2.imread("./../../templates/numbers/10.png", 0)
        res1, loc1 = compare(screenshot, template, 0.9)
        if res1 == 2:
            for pt in zip(*loc1[::-1]):
                sc = {"x": pt[0], "y": pt[1]}
        if not sc:
            return None
        cropped = np.float32(screenshot)[sc["y"]:sc["y"] + 54, sc["x"]:sc["x"] + 385]
        res2, loc2 = compare(cropped, frame_end, 0.9)
        if res2 == 2:
            for pt in zip(*loc2[::-1]):
                cc = {"x": pt[0], "y": pt[1]}
        if not cc:
            return None
        rubber_crop = np.float32(screenshot)[sc["y"] + 41:sc["y"] + 51, sc["x"] + 17:sc["x"] + cc["x"] - 2]
        while not slc:
            res3, loc3 = compare(rubber_crop, slash, 0.9)
            if res3 == 1:
                for pt in zip(*loc3[::-1]):
                    slc = {"x": pt[0], "y": pt[1]}
            if not slc:
                return None
        i = 0
        while i < 11:
            push_away_slash = cropped[slc["y"] + 41:slc["y"] + 51, slc["x"] - 23:slc["x"] - 15]
            push_away_slash_gray = cv2.cvtColor(push_away_slash, cv2.COLOR_BGR2GRAY)
            j = 0
            while j < 11:
                num = cv2.imread("./../../templates/numbers/" + str(j) + ".png", 0)
                res4 = cv2.matchTemplate(push_away_slash_gray, np.float32(num), cv2.TM_CCOEFF_NORMED)
                if res4 > 0.8:
                    hp_min_max += nums[j]
                j += 1
            slc["x"] = slc["x"] + 8
            i += 1
        hp_min_max = hp_min_max.split("/")
        hp_min = hp_min_max[0]
        hp_max = hp_min_max[1]
        percent = round(100 * int(hp_min) / int(hp_max))
        return percent

    def get_target_hp(self):
        """Получить уровень hp цели"""
        hp_color = [[111, 23, 19], [111, 23, 20]]
        wc = {}
        cc = {}
        filled_red_pixels = 0
        template = cv2.imread('./../../templates/frames/target_bar_close.png', 0)
        template_open = cv2.imread('./../../templates/frames/target_bar_open.png', 0)
        frame_end = cv2.imread('./../../templates/frames/frame_end.png', 0)
        res1, loc1 = compare(screenshot, template, 0.9)
        res2, loc2 = compare(screenshot, template_open, 0.9)
        if res1 == 2:
            for pt in zip(*loc1[::-1]):
                wc = {"x": pt[0], "y": pt[1]}
        if res2 == 2:
            for pt in zip(*loc2[::-1]):
                wc = {"x": pt[0], "y": pt[1]}
        if not wc:
            return None
        cropped = np.float32(screenshot)[wc["y"]:wc["y"] + 45, wc["x"]:wc["x"] + 385]
        res3, loc3 = compare(cropped, frame_end, 0.9)
        if res3 == 2:
            for pt in zip(*loc3[::-1]):
                cc = {"x": pt[0], "y": pt[1]}
        if not cc:
            return None
        rubber_crop = np.float32(screenshot)[wc["y"] + 28:wc["y"] + 29, wc["x"] + 17:wc["x"] + cc["x"] - 3]
        pixels = rubber_crop[0].tolist()
        for pixel in pixels:
            if pixel == hp_color[0]:
                filled_red_pixels += 1
            elif pixel == hp_color[1]:
                filled_red_pixels += 1
        percent = round(100 * filled_red_pixels / len(pixels))
        return percent

    def click_on_the_button_with_the_mouse(self, le, bo, panel, button):
        """
        Клик по кнопке на панели скиллов
        :param le: отступ слева до экрана игры
        :param bo: отступ снизу до экрана игры
        :param panel: порядковый номер панели комманд снизу-вверх
        :param button: порядковый номер кнопки
        """
        x1 = 391
        y2 = 28
        z = 18
        panel = panel - 1
        skill_panel = [[{'1': [le + x1 + 15, bo - y2 - z], '2': [le + x1 + 52, bo - y2 - z],
                         '3': [le + x1 + 89, bo - y2 - z], '4': [le + x1 + 126, bo - y2 - z],
                         '5': [le + x1 + 170, bo - y2 - z], '6': [le + x1 + 207, bo - y2 - z],
                         '7': [le + x1 + 244, bo - y2 - z], '8': [le + x1 + 281, bo - y2 - z],
                         '9': [le + x1 + 327, bo - y2 - z], '10': [le + x1 + 364, bo - y2 - z],
                         '11': [le + x1 + 401, bo - y2 - z], '12': [le + x1 + 438, bo - y2 - z]}],
                       [{'1': [le + x1 + 15, bo - y2 - z - 48], '2': [le + x1 + 52, bo - y2 - z - 48],
                         '3': [le + x1 + 89, bo - y2 - z - 48], '4': [le + x1 + 126, bo - y2 - z - 48],
                         '5': [le + x1 + 170, bo - y2 - z - 48], '6': [le + x1 + 207, bo - y2 - z - 48],
                         '7': [le + x1 + 244, bo - y2 - z - 48], '8': [le + x1 + 281, bo - y2 - z - 48],
                         '9': [le + x1 + 327, bo - y2 - z - 48], '10': [le + x1 + 364, bo - y2 - z - 48],
                         '11': [le + x1 + 401, bo - y2 - z - 48], '12': [le + x1 + 438, bo - y2 - z - 48]}],
                       [{'1': [le + x1 + 15, bo - y2 - z - 94], '2': [le + x1 + 52, bo - y2 - z - 94],
                         '3': [le + x1 + 89, bo - y2 - z - 94], '4': [le + x1 + 126, bo - y2 - z - 94],
                         '5': [le + x1 + 170, bo - y2 - z - 94], '6': [le + x1 + 207, bo - y2 - z - 94],
                         '7': [le + x1 + 244, bo - y2 - z - 94], '8': [le + x1 + 281, bo - y2 - z - 94],
                         '9': [le + x1 + 327, bo - y2 - z - 94], '10': [le + x1 + 364, bo - y2 - z - 94],
                         '11': [le + x1 + 401, bo - y2 - z - 94], '12': [le + x1 + 438, bo - y2 - z - 94]}],
                       [{'1': [le + x1 + 15, bo - y2 - z - 136], '2': [le + x1 + 52, bo - y2 - z - 136],
                         '3': [le + x1 + 89, bo - y2 - z - 136], '4': [le + x1 + 126, bo - y2 - z - 136],
                         '5': [le + x1 + 170, bo - y2 - z - 136], '6': [le + x1 + 207, bo - y2 - z - 136],
                         '7': [le + x1 + 244, bo - y2 - z - 136], '8': [le + x1 + 281, bo - y2 - z - 136],
                         '9': [le + x1 + 327, bo - y2 - z - 136], '10': [le + x1 + 364, bo - y2 - z - 136],
                         '11': [le + x1 + 401, bo - y2 - z - 136], '12': [le + x1 + 438, bo - y2 - z - 136]}]]

        click(x=skill_panel[panel][0][str(button)][0], y=skill_panel[panel][0][str(button)][1])

    def press_the_button_with_the_keyboard(self, press_f_key: int, loot=False):
        """
        Нажатие определенной клавиши F
        :param press_f_key: порядковый номер клавиши F
        :param loot: зажатие клавиши F
        """
        press_f_key -= 1
        loot_time = random.uniform(1.120, 1.610)
        press_time = random.uniform(0.049, 0.151)
        if loot:
            self.press_key(press_f_key, loot_time)
        else:
            self.press_key(press_f_key, press_time)

    def press_key(self, key, hold):
        """
        Очеловеченное нажатие на клавишу
        :param key: номер кнопки F
        :param hold: время зажатия клавиши
        """
        autoit.send("{" + self.buttons[key] + " down}")
        time.sleep(hold)
        autoit.send("{" + self.buttons[key] + " up}")

    def find_target(self, le, to, ri, bo):
        """
        Ищет цель на экране
        :param le: левый край экрана
        :param to: верхний край экрана
        :param ri: правый край экрана
        :param bo: нижний край экрана
        :return: точки координат целей
        """
        image = np.array(screenshot)
        w = ri - le
        h = bo - to
        image[0:205, 855:w] = (0, 0, 0)
        image[0:h, 0:100] = (0, 0, 0)
        image[0:h, w - 100:w] = (0, 0, 0)
        image[h - 208:h, 0:w] = (0, 0, 0)
        image[0:50, 0:w] = (0, 0, 0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, threshold1 = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 5))
        closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)
        closed = cv2.dilate(closed, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours

    def take_aim(self, contours, le, to):
        """
        Наводит мышь на цель
        :param contours:
        :param le: левый край экрана
        :param to: верхний край экрана
        :return: True, если цель получена
        """
        for contour in contours:
            lt = list(contour[contour[:, :, 0].argmin()][0])
            rt = list(contour[contour[:, :, 0].argmax()][0])
            x = int(round((rt[0] + lt[0]) / 2))
            y = contour[0][0][1]
            bezier_movements(le + x, to + y + 55)
            time.sleep(0.3)
            cropped = np.array(screenshot)[y - 20:y + 30, contour[0][0][0] - 50:contour[0][0][0] + 180]
            target_visible = cv2.imread('./../../templates/frames/template_target.png', 0)
            res, loc = compare(cropped, target_visible, 0.9)
            if res >= 2:
                return True
        return False


def attack_target():
    def mob_attack():
        pers.click_on_the_button_with_the_mouse(left, bot, 1, 1)  # Атака (панель 1, кнопка 1)
        while True:
            if target_hp == 0:
                break

    pers.click_on_the_button_with_the_mouse(left, bot, 2, random.randint(1, 2))  # Ближайшая цель (панель 1, кнопка 4)
    time.sleep(0.5)
    if target_hp is None or target_hp == 0:
        return False
    else:
        mob_attack()


pers = Personage()
hid = pers.windows[0]
# img, l, t, r, b = get_screenshot(hid)
focus_windows(hid)
pers.stream(hid)
time.sleep(1)
targets = pers.find_target(left, top, right, bot)
if pers.take_aim(targets, left, top):
    click()
else:
    drag_cam(left, top, right, bot)
# time.sleep(1)
targets = pers.find_target(left, top, right, bot)
pers.take_aim(targets, left, top)
# pers.take_aim(screenshot, left, top, right, bot)
# pers.stream(hid)
# time.sleep(1.3)

# pers.hp_stream()
# pers.target_hp_stream()

# pers.press_the_button_with_the_keyboard(press_f_key=6)

# while True:
#     print(target_hp, self_hp, left, top, right, bot)
#     time.sleep(1)

# move_to_center(left, top, right, bot)
# for i in range(10):
#     chaotic_movements()
# move_to_center(left, top, right, bot)
# drag_cam(left, top, right, bot)
