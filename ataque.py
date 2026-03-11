import random

from config import Config
from ocr_utils import OCRManager
from utils import MouseUtils, TimeUtils


class AtaqueManager:
    def __init__(self):
        self.ocr = OCRManager()
        self.ultimo_npc_abs = None
        self.camera_centrada = False

    def iniciar_ataque(self, deteccao_npc):
        # coordenadas YOLO são relativas ao frame (MAP_REGION). converte para absoluto.
        x_rel, y_rel = deteccao_npc["centro"]
        x_abs, y_abs = MouseUtils.coordenada_absoluta(x_rel, y_rel)

        bbox = deteccao_npc.get("bbox")
        bbox_abs = None
        if bbox:
            x1, y1, x2, y2 = bbox
            x1a, y1a = MouseUtils.coordenada_absoluta(x1, y1)
            x2a, y2a = MouseUtils.coordenada_absoluta(x2, y2)
            bbox_abs = (x1a, y1a, x2a, y2a)

        self.ultimo_npc_abs = {"centro": (x_abs, y_abs), "bbox": bbox_abs}

        # 1) seleção precisa no centro do alvo
        MouseUtils.clique_humanizado_rapido(x_abs, y_abs, absoluto=True)
        TimeUtils.espera_aleatoria(0.15, 0.2)
        MouseUtils.press_key_for("e", 0.06)

        # 2) entrar no estado de ataque confirmado (controlado por OCR superior)
        return self.monitorar_ataque()

    def monitorar_ataque(self):
        while True:
            if self.ocr.tem_texto_barra_superior():
                self._cliques_variados_bbox()
                TimeUtils.espera_aleatoria(0.25, 0.35)
                continue

            self._resetar_estado()
            return "EXPLORAR"

    def _cliques_variados_bbox(self):
        if self.ultimo_npc_abs and self.ultimo_npc_abs.get("bbox"):
            x1, y1, x2, y2 = self.ultimo_npc_abs["bbox"]
            alvo_x = (x1 + x2) // 2 + random.randint(-6, 6)
            alvo_y = (y1 + y2) // 2 + random.randint(-6, 6)
        elif self.ultimo_npc_abs:
            alvo_x, alvo_y = self.ultimo_npc_abs["centro"]
        else:
            alvo_x = Config.MAP_REGION["left"] + Config.MAP_REGION["width"] // 2
            alvo_y = Config.MAP_REGION["top"] + Config.MAP_REGION["height"] // 2

        MouseUtils.clique_humanizado_rapido(alvo_x, alvo_y, absoluto=True)
        MouseUtils.press_key_for("e", 0.05)

    def _resetar_estado(self):
        self.ultimo_npc_abs = None
        self.camera_centrada = False
