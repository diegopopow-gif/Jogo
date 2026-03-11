import json
import os
import numpy as np


class Config:
    # ------------------ Regiões do jogo ------------------ #
    MAP_REGION = {"left": 275, "top": 159, "width": 817, "height": 450}
    BARRA_SUPERIOR_REGION = {"left": 1197, "top": 201, "width": 168, "height": 25}
    BARRA_LATERAL_REGION = {"left": 1195, "top": 287, "width": 168, "height": 30}
    TELA_MORTE_REGION = {"left": 713, "top": 373, "width": 151, "height": 200}

    # ------------------ YOLO ------------------ #
    MODEL_PATH = r"C:\Users\ludju\runs\detect\train_cpu_otimizado22\weights\last.pt"
    CONFIDENCE_THRESHOLD = 0.25
    CLASS_NAMES = {
        0: "AMIGO",
        1: "INIMIGO",
        2: "NPC",
        3: "NPCEVENTO",
        4: "baucinza",
        5: "baudourado",
        6: "ilhaguilda",
    }
    CLASS_THRESHOLDS = {"ilhaguilda": 0.45, "AMIGO": 0.08, "INIMIGO": 0.1, "NPC": 0.3}
    PRIORIDADES = ["NPCEVENTO", "NPC", "baudourado", "baucinza"]

    # ------------------ Tempo e delays ------------------ #
    TEMPO_ESPERA_COLETAR = (3, 4)
    DELAY_BARRA_DEFESA = 1
    EXTRA_RANGE_ATAQUE = 10
    TEMPO_ENTRE_EVASOES = 2
    BRILHO_THRESHOLD = 24

    # ------------------ Cores (HSV) ------------------ #
    LOWER_BLUE = np.array([90, 50, 50])
    UPPER_BLUE = np.array([130, 255, 255])

    @classmethod
    def carregar_configuracao(cls, arquivo="config.json"):
        if not os.path.exists(arquivo):
            return

        with open(arquivo, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        for key, value in config_data.items():
            # aceita variação de caixa no JSON (ex.: brilho_threshold)
            destino = key if hasattr(cls, key) else key.upper()
            if hasattr(cls, destino):
                setattr(cls, destino, value)

        print("✅ Configuração carregada do arquivo")


Config.carregar_configuracao()
