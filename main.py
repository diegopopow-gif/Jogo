import argparse
import logging
import random
import sys
import time

import cv2
import keyboard
import numpy as np
from mss import mss

from ataque import AtaqueManager
from config import Config
from defesa import DefesaManager
from evasao import EvasaoManager
from exploracao import ExploracaoManager
from health_check import HealthCheck
from ocr_utils import OCRManager
from reparacao import ReparacaoManager

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])


class BotNavio:
    def __init__(self, modo_teste=False):
        self.sct = mss()
        self.ocr = OCRManager()
        self.exploracao = ExploracaoManager()
        self.ataque = AtaqueManager()
        self.defesa = DefesaManager()
        self.evasao = EvasaoManager()
        self.reparacao = ReparacaoManager()
        self.health_check = HealthCheck()

        self.estado_atual = "EXPLORAR"
        self.executando = True
        self.modo_teste = modo_teste

    def capturar_tela(self):
        screenshot = self.sct.grab(Config.MAP_REGION)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)

    def verificar_pausa(self):
        if keyboard.is_pressed("p"):
            logging.info("⏸️ Bot pausado. Pressione 'P' para continuar...")
            while keyboard.is_pressed("p"):
                time.sleep(0.1)
            logging.info("▶️ Bot retomado")
            return True
        return False

    def executar(self):
        logging.info("🤖 Bot Navio iniciado!")
        if not self.health_check.verificar_saude_inicial():
            logging.error("❌ Verificação de saúde falhou.")
            return

        if self.modo_teste:
            logging.info("🔧 Modo teste ativado")
            return

        keyboard.press_and_release("1")

        try:
            while self.executando:
                if self.verificar_pausa():
                    continue

                # prioridade 1: reparação
                if self.reparacao.verificar_tela_morte():
                    logging.info("💀 Tela de morte detectada, reparando...")
                    self.reparacao.executar_reparacao()
                    self.estado_atual = "EXPLORAR"
                    continue

                # prioridade 2: ataque confirmado por OCR superior
                if self.ocr.tem_texto_barra_superior():
                    self.estado_atual = "ATACAR"
                    self.ataque.monitorar_ataque()
                    self.estado_atual = "EXPLORAR"
                    continue

                frame = self.capturar_tela()

                # prioridade 3: defesa por texto lateral (exceto torre/desconhecido)
                if self.defesa.verificar_defesa():
                    self.defesa.executar_defesa()
                    continue

                resultado, deteccao = self.exploracao.executar_ciclo_exploracao(frame)

                if resultado == "ATACAR" and deteccao:
                    self.estado_atual = "ATACAR"
                    self.ataque.iniciar_ataque(deteccao)
                    self.estado_atual = "EXPLORAR"
                elif resultado == "EVADIR" and deteccao:
                    self.estado_atual = "EVADIR"
                    if deteccao.get("classe") == "ilhaguilda":
                        self.evasao.evadir_ilhaguilda(deteccao)
                    else:
                        self.evasao.evadir_ocr()
                    self.estado_atual = "EXPLORAR"
                else:
                    self.estado_atual = "EXPLORAR"

                time.sleep(random.uniform(0.05, 0.12))

        except KeyboardInterrupt:
            logging.info("🛑 Bot interrompido")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--teste", action="store_true")
    parser.add_argument("--config", type=str)
    args = parser.parse_args()

    if args.config:
        Config.carregar_configuracao(args.config)

    bot = BotNavio(modo_teste=args.teste)
    bot.executar()
