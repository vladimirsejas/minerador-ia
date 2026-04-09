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

# Exemplo de uso:
analisador = Analisador()
resultado = analisador.analisar(dados)

# Impressão separada
if "mensagem" in resultado:
    print("[ANÁLISE]", resultado["mensagem"])
else:
    print("\n" + "=" * 50)
    print("        ANÁLISE DOS DADOS COLETADOS")
    print("=" * 50)
    print(f"\n Total de artigos coletados: {resultado['total_artigos']}")
    print("\n Artigos por fonte:")
    for fonte, qtd in resultado["fontes"].items():
        print(f"   {fonte}: {qtd}")
    print("\n Top 10 palavras-chave nos títulos:")
    for palavra, freq in resultado["palavras_chave"]:
        print(f"   '{palavra}': {freq}x")
    print(f"\n Artigos com resumo disponível: {resultado['com_resumo']}/{resultado['total_artigos']}")
    print(f" Artigos com imagem coletada:  {resultado['com_imagem']}/{resultado['total_artigos']}")
    print("=" * 50 + "\n")
