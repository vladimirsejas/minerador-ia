import re
from collections import Counter


class Analisador:
    STOPWORDS = {
        "a", "o", "e", "de", "do", "da", "em", "um", "uma", "para",
        "the", "of", "and", "in", "to", "is", "for", "on", "with",
        "this", "that", "are", "an", "by", "at", "from", "we", "our",
        "using", "based", "via", "which", "as", "be", "can", "its"
    }

    def analisar(self, dados: list[dict]) -> dict:
        if not dados:
            return {"mensagem": "Sem dados para analisar."}

        fontes = Counter(d.get("fonte", "desconhecida") for d in dados)
        palavras = self._palavras_frequentes(dados)
        com_resumo = sum(1 for d in dados if d.get("resumo"))
        com_imagem = sum(1 for d in dados if d.get("imagem_url"))

        return {
            "total_artigos": len(dados),
            "fontes": dict(fontes),
            "palavras_chave": palavras[:10],
            "com_resumo": com_resumo,
            "com_imagem": com_imagem
        }

    def _palavras_frequentes(self, dados: list[dict]) -> list[tuple]:
        todos_titulos = " ".join(d.get("titulo", "") for d in dados).lower()
        tokens = re.findall(r"\b[a-zA-ZÀ-ú]{4,}\b", todos_titulos)
        filtradas = [t for t in tokens if t not in self.STOPWORDS]
        return Counter(filtradas).most_common()
