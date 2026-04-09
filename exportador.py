import json
import pandas as pd
from datetime import datetime

class Exportador:
    def __init__(self, prefixo: str = "resultados"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.nome_base = f"{prefixo}_{timestamp}"

    def exportar_csv(self, dados: list[dict]) -> str | None:
        if not dados:
            return None
        caminho = f"data/{self.nome_base}.csv"
        df = pd.DataFrame(dados)
        df.to_csv(caminho, index=False, encoding="utf-8-sig")
        return caminho

    def exportar_json(self, dados: list[dict]) -> str | None:
        if not dados:
            return None
        caminho = f"data/{self.nome_base}.json"
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return caminho
