import requests
from bs4 import BeautifulSoup


class Scraper:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def buscar_pagina(self, url: str) -> BeautifulSoup | None:
        try:
            resposta = requests.get(url, headers=self.HEADERS, timeout=10)
            resposta.raise_for_status()
            return BeautifulSoup(resposta.text, "html.parser")
        except requests.exceptions.ConnectionError:
            print(f"[ERRO] Sem conexão para: {url}")
        except requests.exceptions.Timeout:
            print(f"[ERRO] Tempo esgotado para: {url}")
        except requests.exceptions.HTTPError as e:
            print(f"[ERRO] HTTP {e.response.status_code} em: {url}")
        except Exception as e:
            print(f"[ERRO] Inesperado em {url}: {e}")
        return None
