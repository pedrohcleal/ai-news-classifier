from pprint import pprint
import requests
from bs4 import BeautifulSoup
import time
import dateparser
from datetime import datetime
import cloudscraper
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.pipelines import pipeline
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from playwright.sync_api import sync_playwright, Page

retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

cloud_scraper = cloudscraper.create_scraper()
cloud_scraper.mount("http://", adapter)
cloud_scraper.mount("https://", adapter)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def classify(texto):
    model_name = "classla/multilingual-IPTC-news-topic-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer(texto, truncation=True, max_length=512, return_tensors="pt")
    truncated_text = tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
    analisa = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer)
    resultado = analisa(truncated_text)
    return resultado

def check_sense(texto, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer(texto, truncation=True, max_length=120, return_tensors="pt")
    truncated_text = tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
    analisa = pipeline("text-classification", model=model_name, tokenizer=tokenizer)
    resultado = analisa(truncated_text)
    return resultado


def normalize_dt_ref(texto_data):
    data_referencia = datetime.now()

    data = dateparser.parse(
        texto_data,
        languages=['pt'],
        settings={'RELATIVE_BASE': data_referencia}
    )

    if data:
        return data.date().isoformat()  # retorna 'YYYY-MM-DD'
    else:
        return None


def extrair_texto_pagina(url, page: Page):
    try:
        page.goto(url, wait_until="domcontentloaded")  # até 30s para carregar a página
        page.wait_for_load_state("networkidle")  # aguarda fim da carga da rede

        # Remove scripts e estilos (invisíveis)
        page.evaluate("""
            () => {
                const elements = document.querySelectorAll("script, style, noscript");
                elements.forEach(el => el.remove());
            }
        """)

        # Extrai todo o texto visível da página
        texto = page.inner_text("body")
        browser.close()
        return texto.strip()
    except Exception as e:
        print(f"[Playwright Erro ao acessar URL]: {url}\nMotivo: {e}")
        return "Neutro"
    
def scrape_google_news(keyword, model_name, page: Page, num_pages=3) -> list[dict]:
    all_results = []

    for pag_n in range(num_pages):
        start = pag_n * 10
        url = f"https://www.google.com/search?q={keyword}&tbm=nws&start={start}"

        response = cloud_scraper.get(url, headers=HEADERS, timeout=90)
        soup = BeautifulSoup(response.text, "html.parser")

        print(f"\n Página {pag_n + 1} - {url}")

        for article in soup.select(".WlydOe"):
            href = article.get("href")

            title_tag = article.select_one(".n0jPhd.ynAwRc.MBeuO.nDgy9d")
            desc_tag = article.select_one(".GI74Re.nDgy9d")
            dt_pub_tag = article.select_one(".OSrXXb.rbYSKb.LfVVr")

            title = title_tag.text if title_tag else "Título não encontrado"
            description = desc_tag.text if desc_tag else "Descrição não encontrada"
            dt_pub = dt_pub_tag.text if dt_pub_tag else "Data não encontrada"
            page_text = extrair_texto_pagina(href, page)
            
            
            result = {
                "empresa": keyword, 
                "link": href,
                "titulo": title,
                "descrição": description,
                "dt_pub_noticia": normalize_dt_ref(dt_pub),
                "sense_title": check_sense(title, model_name)[0]["label"],
                "sense_description": check_sense(description, model_name)[0]["label"],
                "sense_text_link": check_sense(page_text, model_name)[0]["label"],
                "class_title": classify(title)[0]["label"],
                "class_description": classify(description)[0]["label"],
                "class_text_link": classify(page_text)[0]["label"]
            }

            #pprint(result)
            all_results.append(result)
            #break

        time.sleep(1)

    return all_results

if __name__ == "__main__":
    #model_name = "Harvinder6766/news_sentiment_sentence_v1"
    #model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model_name = "pysentimiento/bertweet-pt-sentiment"
    empresas = ["Komatsu", "Votorantim Cimentos", "Haribo"]
    resultados = []
    import json
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        for brand in empresas:
            resultados.extend(scrape_google_news(brand, model_name, page, num_pages=3))
        
    file_json = model_name.split('/')[1]
    with open(f'{file_json}.json', 'w') as f:
        json.dump(resultados,f,ensure_ascii=False,indent=4)
        
    df = pd.DataFrame(resultados)
    df.to_excel('analises.xlsx', index=False)
    