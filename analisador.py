import re
from collections import Counter


class Analisador:

    STOPWORDS = {
        "a", "o", "e", "de", "do", "da", "em", "um", "uma", "para",
        "the", "of", "and", "in", "to", "a", "is", "for", "on", "with",
        "this", "that", "are", "an", "by", "at", "from", "we", "our",
        "using", "based", "via", "which", "as", "be", "can", "its"
    }

    def analisar(self, dados: list[dict]) -> None:
        if not dados:
            print("[ANÁLISE] Sem dados para analisar.")
            return

        print("\n" + "=" * 50)
        print("        ANÁLISE DOS DADOS COLETADOS")
        print("=" * 50)

        print(f"\n Total de artigos coletados: {len(dados)}")

        fontes = Counter(d.get("fonte", "desconhecida") for d in dados)
        print("\n Artigos por fonte:")
        for fonte, qtd in fontes.most_common():
            print(f"   {fonte}: {qtd}")

        palavras = self._palavras_frequentes(dados)
        print("\n Top 10 palavras-chave nos títulos:")
        for palavra, freq in palavras[:10]:
            print(f"   '{palavra}': {freq}x")

        com_resumo = sum(1 for d in dados if d.get("resumo"))
        print(f"\n Artigos com resumo disponível: {com_resumo}/{len(dados)}")

        com_imagem = sum(1 for d in dados if d.get("imagem_url"))
        print(f" Artigos com imagem coletada:  {com_imagem}/{len(dados)}")
        print("=" * 50 + "\n")

    def _palavras_frequentes(self, dados: list[dict]) -> list[tuple]:
        todos_titulos = " ".join(d.get("titulo", "") for d in dados).lower()
        tokens = re.findall(r"\b[a-zA-ZÀ-ú]{4,}\b", todos_titulos)
        filtradas = [t for t in tokens if t not in self.STOPWORDS]
        return Counter(filtradas).most_common()
