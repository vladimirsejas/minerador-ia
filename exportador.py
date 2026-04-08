import json
import pandas as pd
from datetime import datetime


class Exportador:

    def __init__(self, prefixo: str = "resultados"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.nome_base = f"{prefixo}_{timestamp}"

    def exportar_csv(self, dados: list[dict]) -> str:
        if not dados:
            print("[EXPORTADOR] Nenhum dado para exportar em CSV.")
            return ""
        caminho = f"data/{self.nome_base}.csv"
        df = pd.DataFrame(dados)
        df.to_csv(caminho, index=False, encoding="utf-8-sig")
        print(f"[EXPORTADOR] CSV salvo: {caminho} ({len(dados)} registros)")
        return caminho

    def exportar_json(self, dados: list[dict]) -> str:
        if not dados:
            print("[EXPORTADOR] Nenhum dado para exportar em JSON.")
            return ""
        caminho = f"data/{self.nome_base}.json"
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"[EXPORTADOR] JSON salvo: {caminho}")
        return caminho
