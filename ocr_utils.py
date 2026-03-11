import re

import cv2
import numpy as np
import pytesseract
from mss import mss

from config import Config


class OCRManager:
    def __init__(self):
        self.sct = mss()
        self.ultimo_texto_superior = ""
        self.ultimo_texto_lateral = ""

    def _extrair_texto_da_regiao(self, region):
        screenshot = self.sct.grab(region)
        img = np.array(screenshot)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        return pytesseract.image_to_string(thresh, config="--psm 7").strip()

    def tem_texto_barra_superior(self):
        texto = self._extrair_texto_da_regiao(Config.BARRA_SUPERIOR_REGION)
        if self._texto_valido(texto):
            self.ultimo_texto_superior = texto
            return True
        self.ultimo_texto_superior = ""
        return False

    def verificar_barra_lateral(self):
        texto = self._extrair_texto_da_regiao(Config.BARRA_LATERAL_REGION)
        if self._texto_valido(texto):
            self.ultimo_texto_lateral = texto
            return True
        self.ultimo_texto_lateral = ""
        return False

    def get_texto_barra_lateral(self, atualizar=False):
        if atualizar:
            self.verificar_barra_lateral()
        return self.ultimo_texto_lateral

    def get_texto_barra_superior(self, atualizar=False):
        if atualizar:
            self.tem_texto_barra_superior()
        return self.ultimo_texto_superior

    def texto_lateral_indica_torre_ou_desconhecido(self):
        txt = self.get_texto_barra_lateral(atualizar=True).lower()
        if not txt:
            return False
        return ("torre" in txt and "nivel" in txt) or ("inimigo" in txt and "descon" in txt)

    def _texto_valido(self, texto):
        if not texto:
            return False
        texto = texto.strip()
        if len(texto) < 3:
            return False

        # Remove ruído óbvio de OCR (repetições de uma mesma letra e caracteres aleatórios)
        apenas_letras = re.sub(r"[^a-zA-ZÀ-ÿ ]", "", texto)
        palavras = [p for p in apenas_letras.split() if len(p) >= 2]
        if not palavras:
            return False
        if len(set(apenas_letras.replace(" ", "").lower())) <= 2 and len(apenas_letras) >= 5:
            return False
        return True
