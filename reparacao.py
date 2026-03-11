import time

import cv2
import numpy as np
import pyautogui
from mss import mss

from config import Config
from utils import MouseUtils, TimeUtils


class ReparacaoManager:
    def __init__(self):
        self.sct = mss()
        self.brilho_threshold = getattr(Config, "BRILHO_THRESHOLD", 24)

    def verificar_tela_morte(self):
        try:
            screenshot = self.sct.grab(Config.TELA_MORTE_REGION)
            frame = np.array(screenshot)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brilho_medio = np.mean(gray)
            return brilho_medio < self.brilho_threshold
        except Exception:
            return False

    def executar_reparacao(self):
        x_centro = Config.TELA_MORTE_REGION["left"] + Config.TELA_MORTE_REGION["width"] // 2
        y_centro = Config.TELA_MORTE_REGION["top"] + Config.TELA_MORTE_REGION["height"] // 2

        MouseUtils.clique_humanizado_rapido(x_centro, y_centro, absoluto=True)
        TimeUtils.espera_aleatoria(3, 0.2)
        TimeUtils.espera_aleatoria(2, 0.2)
        pyautogui.press("r")

        time.sleep(8)
        for _ in range(10):
            if not self.verificar_tela_morte():
                return
            time.sleep(1)
