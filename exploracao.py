import random

import cv2

from config import Config
from ocr_utils import OCRManager
from utils import MouseUtils, TimeUtils
from yolo_detector import YOLODetector


class ExploracaoManager:
    def __init__(self):
        self.yolo = YOLODetector()
        self.ocr = OCRManager()

    def executar_ciclo_exploracao(self, frame):
        deteccoes = self.yolo.detectar_objetos(frame)

        # prioridade máxima no fluxo da exploração: evasão por visão
        for d in deteccoes:
            if d["classe"] in ["ilhaguilda", "INIMIGO"]:
                return "EVADIR", d

        for d in deteccoes:
            if d["classe"] in ["NPCEVENTO", "NPC"]:
                return "ATACAR", d

        for d in deteccoes:
            if d["classe"] in ["baudourado", "baucinza"]:
                x_rel, y_rel = d["centro"]
                x_abs, y_abs = MouseUtils.coordenada_absoluta(x_rel, y_rel)
                MouseUtils.clique_humanizado_rapido(x_abs, y_abs, absoluto=True)
                TimeUtils.espera_aleatoria(*Config.TEMPO_ESPERA_COLETAR)
                return "BAU", d

        # double-check OCR lateral para torre/inimigo desconhecido
        if self.ocr.texto_lateral_indica_torre_ou_desconhecido():
            return "EVADIR", {"classe": "ilhaguilda"}

        ponto = self._encontrar_ponto_azul(frame)
        if ponto:
            x_abs, y_abs = MouseUtils.coordenada_absoluta(*ponto)
            MouseUtils.clique_humanizado_rapido(x_abs, y_abs, absoluto=True)
            TimeUtils.espera_aleatoria(0.6, 0.2)
            return "EXPLORAR", None

        x = random.randint(Config.MAP_REGION["left"] + 10, Config.MAP_REGION["left"] + Config.MAP_REGION["width"] - 10)
        y = random.randint(Config.MAP_REGION["top"] + 10, Config.MAP_REGION["top"] + Config.MAP_REGION["height"] - 10)
        MouseUtils.clique_humanizado_rapido(x, y, absoluto=True)
        TimeUtils.espera_aleatoria(0.6, 0.2)
        return "EXPLORAR", None

    def _encontrar_ponto_azul(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, Config.LOWER_BLUE, Config.UPPER_BLUE)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        pontos = []
        for c in contours:
            if cv2.contourArea(c) <= 20:
                continue
            m = cv2.moments(c)
            if m["m00"] == 0:
                continue
            pontos.append((int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])))
        return random.choice(pontos) if pontos else None
