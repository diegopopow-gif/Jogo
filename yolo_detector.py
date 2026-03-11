from ultralytics import YOLO

from config import Config


class YOLODetector:
    def __init__(self):
        self.model = YOLO(Config.MODEL_PATH)
        self.class_names = Config.CLASS_NAMES

    def detectar_objetos(self, frame):
        resultados = self.model(frame, conf=Config.CONFIDENCE_THRESHOLD)
        deteccoes = []

        for resultado in resultados:
            boxes = resultado.boxes
            if boxes is None:
                continue
            for box in boxes:
                confianca = box.conf.item()
                classe_id = int(box.cls.item())
                classe_nome = self.class_names.get(classe_id, "DESCONHECIDO")
                threshold = Config.CLASS_THRESHOLDS.get(classe_nome, Config.CONFIDENCE_THRESHOLD)
                if confianca < threshold:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                centro_x, centro_y = (x1 + x2) // 2, (y1 + y2) // 2
                deteccoes.append(
                    {
                        "classe": classe_nome,
                        "bbox": (x1, y1, x2, y2),
                        "centro": (centro_x, centro_y),
                        "confianca": confianca,
                    }
                )

        return self._ordenar_por_prioridade(deteccoes)

    def _ordenar_por_prioridade(self, deteccoes):
        deteccoes.sort(
            key=lambda x: Config.PRIORIDADES.index(x["classe"]) if x["classe"] in Config.PRIORIDADES else len(Config.PRIORIDADES)
        )
        return deteccoes
