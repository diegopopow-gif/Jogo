import random
import time

import pyautogui

from config import Config


class MouseUtils:
    @staticmethod
    def coordenada_absoluta(x_rel, y_rel):
        x_abs = x_rel + Config.MAP_REGION["left"]
        y_abs = y_rel + Config.MAP_REGION["top"]

        x_abs = max(Config.MAP_REGION["left"], min(Config.MAP_REGION["left"] + Config.MAP_REGION["width"] - 1, x_abs))
        y_abs = max(Config.MAP_REGION["top"], min(Config.MAP_REGION["top"] + Config.MAP_REGION["height"] - 1, y_abs))
        return int(x_abs), int(y_abs)

    @staticmethod
    def _bezier_point(t, points):
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        x = (
            mt3 * points[0][0]
            + 3 * mt2 * t * points[1][0]
            + 3 * mt * t2 * points[2][0]
            + t3 * points[3][0]
        )
        y = (
            mt3 * points[0][1]
            + 3 * mt2 * t * points[1][1]
            + 3 * mt * t2 * points[2][1]
            + t3 * points[3][1]
        )
        return int(x), int(y)

    @staticmethod
    def _gerar_curva(start_x, start_y, end_x, end_y, curvature=0.05):
        dx = end_x - start_x
        dy = end_y - start_y
        control1 = (start_x + dx * curvature, start_y + dy * curvature)
        control2 = (start_x + dx * (1 - curvature), start_y + dy * (1 - curvature))
        return [(start_x, start_y), control1, control2, (end_x, end_y)]

    @staticmethod
    def mover_mouse_instantaneo(x, y, steps=15, duration=None, absoluto=False):
        if not absoluto:
            x, y = MouseUtils.coordenada_absoluta(x, y)

        if duration is None:
            duration = random.uniform(0.4, 1.1)

        current_x, current_y = pyautogui.position()
        distancia = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5

        if distancia < 10:
            pyautogui.moveTo(x, y, duration=random.uniform(0.05, 0.15), _pause=False)
            return

        control_points = MouseUtils._gerar_curva(current_x, current_y, x, y)
        for i in range(steps + 1):
            t = i / steps
            px, py = MouseUtils._bezier_point(t, control_points)
            if i == 0:
                continue
            pyautogui.moveTo(px, py, duration=duration / steps, _pause=False)

    @staticmethod
    def clique_humanizado_rapido(x, y, duplo=False, absoluto=False):
        MouseUtils.mover_mouse_instantaneo(x, y, absoluto=absoluto)
        time.sleep(random.uniform(0.2, 0.4))
        if duplo:
            pyautogui.doubleClick()
        else:
            pyautogui.click()
        time.sleep(random.uniform(0.1, 0.3))

    @staticmethod
    def press_key_for(tecla, segundos):
        pyautogui.keyDown(tecla)
        time.sleep(segundos)
        pyautogui.keyUp(tecla)


class TimeUtils:
    @staticmethod
    def espera_aleatoria(tempo_base, variacao=0.1):
        tempo = max(0.01, tempo_base * random.uniform(1 - variacao, 1 + variacao))
        time.sleep(tempo)
