from bs4 import BeautifulSoup

class Parser:

    def extrair_artigos_arxiv(self, soup: BeautifulSoup) -> list[dict]:
        artigos = []
        try:
            resultados = soup.find_all("li", class_="arxiv-result")
            for item in resultados:
                titulo = self._texto(item, "p", class_="title")
                autores = self._texto(item, "p", class_="authors")
                resumo = self._texto(item, "span", class_="abstract-full")

                link_tag = item.find("p", class_="list-title")
                link = ""
                if link_tag:
                    a = link_tag.find("a")
                    link = a["href"] if a else ""

                data = self._texto(item, "p", class_="is-size-7")

                artigos.append({
                    "titulo": titulo,
                    "autores": autores.replace("Authors:", "").strip(),
                    "resumo": resumo.strip(),
                    "link": f"https://arxiv.org{link}" if link.startswith("/") else link,
                    "data": data.split(";")[0].strip() if data else "",
                    "imagem_url": self._extrair_imagem(item),
                    "fonte": "arXiv"
                })
        except Exception as e:
            print(f"[PARSER] Erro ao extrair artigos: {e}")
        return artigos

    def _texto(self, elemento, tag: str, **kwargs) -> str:
        try:
            found = elemento.find(tag, **kwargs)
            return found.get_text(separator=" ", strip=True) if found else ""
        except Exception:
            return ""

    def _extrair_imagem(self, elemento) -> str:
        try:
            img = elemento.find("img")
            return img["src"] if img and img.get("src") else ""
        except Exception:
            return ""

    def extrair_artigos_scielo(self, soup):
        artigos = []
        try:
            resultados = soup.find_all("div", class_="item")
            for item in resultados:
                titulo_tag = item.find("a")
                titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""
                link = titulo_tag["href"] if titulo_tag else ""

                resumo_tag = item.find("div", class_="abstract")
                resumo = resumo_tag.get_text(strip=True) if resumo_tag else ""

                artigos.append({
                    "titulo": titulo,
                    "autores": "",
                    "resumo": resumo,
                    "link": link,
                    "data": "",
                    "imagem_url": "",
                    "fonte": "SciELO"
                })
        except Exception as e:
            print(f"[SCIELO ERRO] {e}")
        return artigos
