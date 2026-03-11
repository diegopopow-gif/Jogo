import time

from config import Config
from ocr_utils import OCRManager
from utils import MouseUtils, TimeUtils


class DefesaManager:
    def __init__(self):
        self.ocr = OCRManager()
        self.ultimo_ataque_defesa = 0

    def executar_defesa(self):
        agora = time.time()
        if agora - self.ultimo_ataque_defesa < Config.DELAY_BARRA_DEFESA:
            return
        self.ultimo_ataque_defesa = agora

        TimeUtils.espera_aleatoria(2.0, 0.3)

        x_centro = Config.BARRA_LATERAL_REGION["left"] + Config.BARRA_LATERAL_REGION["width"] // 2
        y_centro = Config.BARRA_LATERAL_REGION["top"] + Config.BARRA_LATERAL_REGION["height"] // 2
        MouseUtils.clique_humanizado_rapido(x_centro, y_centro, duplo=True, absoluto=True)

    def verificar_defesa(self):
        # sempre atualiza OCR lateral e superior antes de decidir
        texto = self.ocr.get_texto_barra_lateral(atualizar=True)
        superior = self.ocr.tem_texto_barra_superior()

        if not texto or superior:
            return False

        txt = texto.lower()
        if ("torre" in txt and "nivel" in txt) or ("inimigo" in txt and "descon" in txt):
            return False

        return True
