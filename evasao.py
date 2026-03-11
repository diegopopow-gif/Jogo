import logging
import random
import time

from config import Config
from utils import MouseUtils, TimeUtils

logger = logging.getLogger(__name__)


class EvasaoManager:
    def __init__(self):
        self.ultima_evasao = 0
        self.tempo_entre = getattr(Config, "TEMPO_ENTRE_EVASOES", 2)

    def _pode_evadir(self):
        return (time.time() - self.ultima_evasao) >= self.tempo_entre

    def evadir_ilhaguilda(self, deteccao):
        if not self._pode_evadir():
            return
        centro_x, centro_y = deteccao.get("centro", (Config.MAP_REGION["width"] // 2, Config.MAP_REGION["height"] // 2))
        # centro relativo ao MAP_REGION
        metade_x = Config.MAP_REGION["width"] // 2
        metade_y = Config.MAP_REGION["height"] // 2

        horiz = "d" if centro_x < metade_x else "a"
        vert = "s" if centro_y < metade_y else "w"

        dur = random.uniform(0.12, 0.28)
        MouseUtils.press_key_for(horiz, dur)
        MouseUtils.press_key_for(vert, dur)

        x = random.randint(Config.MAP_REGION["left"] + 10, Config.MAP_REGION["left"] + Config.MAP_REGION["width"] - 10)
        y = random.randint(Config.MAP_REGION["top"] + 10, Config.MAP_REGION["top"] + Config.MAP_REGION["height"] - 10)
        MouseUtils.clique_humanizado_rapido(x, y, absoluto=True)

        self.ultima_evasao = time.time()
        TimeUtils.espera_aleatoria(1.0, 0.3)
        logger.info("🏝️ Evasão por YOLO executada")

    def evadir_ocr(self):
        if not self._pode_evadir():
            return
        for _ in range(random.randint(1, 3)):
            teclas = random.choice([["w"], ["s"], ["a"], ["d"], ["w", "a"], ["w", "d"], ["s", "a"], ["s", "d"]])
            dur = random.uniform(0.1, 0.4)
            for t in teclas:
                MouseUtils.press_key_for(t, dur)

            x = random.randint(Config.MAP_REGION["left"] + 10, Config.MAP_REGION["left"] + Config.MAP_REGION["width"] - 10)
            y = random.randint(Config.MAP_REGION["top"] + 10, Config.MAP_REGION["top"] + Config.MAP_REGION["height"] - 10)
            MouseUtils.clique_humanizado_rapido(x, y, absoluto=True)

        self.ultima_evasao = time.time()
        TimeUtils.espera_aleatoria(1.0, 0.3)
        logger.info("⚠️ Evasão por OCR executada")
