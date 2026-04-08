from scraper import Scraper
from parser import Parser
from exportador import Exportador
from analisador import Analisador
import glob
import pandas as pd


# ─────────────────────────────
# TERMOS BASE
# ─────────────────────────────

TERMOS_BUSCA = list(dict.fromkeys([
    "artificial intelligence datacenter",
    "deep learning infrastructure",
    "large language models",
    "inteligencia artificial",
    "centro de dados inteligencia artificial",
    "infraestrutura aprendizado profundo",
    "modelos de linguagem",
    "centros de datos inteligencia artificial",
    "infraestructura aprendizaje profundo",
    "modelos de lenguaje",
]))


BASE_URL = "https://arxiv.org/search/?searchtype=all&query={query}&start=0"
BASE_URL_SCIELO = "https://search.scielo.org/?q={query}&lang=pt"


# ─────────────────────────────
# MENU INTERATIVO
# ─────────────────────────────

def exibir_menu():
    print("\n" + "=" * 60)
    print("   🧠 MINERADOR DE DADOS ACADÊMICOS — IA")
    print("=" * 60)
    print("  1 → Coleta completa (arXiv + SciELO)")
    print("  2 → Analisar último CSV")
    print("  3 → Busca personalizada")
    print("  4 → Ver arquivos gerados")
    print("  0 → Sair")
    print("=" * 60)
    return input("👉 Escolha uma opção: ").strip()


# ─────────────────────────────
# OPÇÃO 1
# ─────────────────────────────

def opcao_coleta_completa():
    print("\n🚀 Iniciando coleta completa...\n")

    scraper = Scraper()
    parser = Parser()
    exportador = Exportador(prefixo="artigos_ia")
    analisador = Analisador()

    todos_artigos = []

    # arXiv
    for termo in TERMOS_BUSCA:
        print(f"\n🔎 Buscando (arXiv): {termo}")
        url = BASE_URL.format(query=termo.replace(" ", "+"))
        soup = scraper.buscar_pagina(url)

        if soup:
            artigos = parser.extrair_artigos_arxiv(soup)
            print(f"✔ {len(artigos)} encontrados")
            todos_artigos.extend(artigos)

    # SciELO
    for termo in TERMOS_BUSCA:
        print(f"\n🔎 Buscando (SciELO): {termo}")
        url = BASE_URL_SCIELO.format(query=termo.replace(" ", "+"))
        soup = scraper.buscar_pagina(url)

        if soup:
            artigos = parser.extrair_artigos_scielo(soup)
            print(f"✔ {len(artigos)} encontrados")
            todos_artigos.extend(artigos)

    # Remover duplicados
    vistos = set()
    unicos = []

    for artigo in todos_artigos:
        if artigo["link"] not in vistos:
            vistos.add(artigo["link"])
            unicos.append(artigo)

    print(f"\n📊 Total único: {len(unicos)} artigos")

    exportador.exportar_csv(unicos)
    exportador.exportar_json(unicos)
    analisador.analisar(unicos)


# ─────────────────────────────
# OPÇÃO 2
# ─────────────────────────────

def opcao_analisar_csv():
    arquivos = sorted(glob.glob("data/artigos_ia_*.csv"), reverse=True)

    if not arquivos:
        print("\n⚠ Nenhum CSV encontrado na pasta data/")
        return

    mais_recente = arquivos[0]
    print(f"\n📂 Analisando: {mais_recente}")

    df = pd.read_csv(mais_recente)
    dados = df.to_dict(orient="records")

    Analisador().analisar(dados)


# ─────────────────────────────
# OPÇÃO 3
# ─────────────────────────────

def opcao_busca_personalizada():
    termo = input("\n🔍 Digite o termo de busca: ").strip()

    if not termo:
        print("⚠ Termo vazio.")
        return

    scraper = Scraper()
    parser = Parser()
    exportador = Exportador(prefixo=f"busca_{termo[:15].replace(' ', '_')}")
    analisador = Analisador()

    artigos = []

    print("\n🔎 Buscando no arXiv...")
    url = BASE_URL.format(query=termo.replace(" ", "+"))
    soup = scraper.buscar_pagina(url)
    if soup:
        artigos.extend(parser.extrair_artigos_arxiv(soup))

    print("🔎 Buscando no SciELO...")
    url = BASE_URL_SCIELO.format(query=termo.replace(" ", "+"))
    soup = scraper.buscar_pagina(url)
    if soup:
        artigos.extend(parser.extrair_artigos_scielo(soup))

    if artigos:
        print(f"\n✔ {len(artigos)} resultados encontrados")
        exportador.exportar_csv(artigos)
        exportador.exportar_json(artigos)
        analisador.analisar(artigos)
    else:
        print("⚠ Nenhum resultado encontrado")


# ─────────────────────────────
# OPÇÃO 4 (NOVO)
# ─────────────────────────────

def opcao_ver_arquivos():
    arquivos = glob.glob("data/*")

    if not arquivos:
        print("\n📂 Pasta data vazia.")
        return

    print("\n📁 Arquivos gerados:")
    for arq in arquivos:
        print(f" - {arq}")


# ─────────────────────────────
# MAIN
# ─────────────────────────────

def main():
    while True:
        opcao = exibir_menu()

        if opcao == "1":
            opcao_coleta_completa()
        elif opcao == "2":
            opcao_analisar_csv()
        elif opcao == "3":
            opcao_busca_personalizada()
        elif opcao == "4":
            opcao_ver_arquivos()
        elif opcao == "0":
            print("\n👋 Encerrando sistema...")
            break
        else:
            print("\n⚠ Opção inválida, tenta de novo.")


if __name__ == "__main__":
    main()