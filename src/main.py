from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd
from config.scraper_configs import cloud_scraper, HEADERS
from utils import utils


def scrape_google_news(keyword, num_pages=3) -> list[dict]:
    all_results = []

    for pag_n in range(num_pages):
        
        start = pag_n * 10
        url = f"https://www.google.com/search?q={keyword}&tbm=nws&start={start}"
        print(f"\n Página {pag_n + 1} - {url}")

        response = cloud_scraper.get(url, headers=HEADERS, timeout=90)
        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.select(".WlydOe")

        for ind, article in enumerate(news):
            print(f'Percorrendo notícias {ind+1} de {len(news)}')
            href = article.get("href")

            title_tag = article.select_one(".n0jPhd.ynAwRc.MBeuO.nDgy9d")
            desc_tag = article.select_one(".GI74Re.nDgy9d")
            dt_pub_tag = article.select_one(".OSrXXb.rbYSKb.LfVVr")

            title = title_tag.text if title_tag else "Título não encontrado"
            description = desc_tag.text if desc_tag else "Descrição não encontrada"
            dt_pub = dt_pub_tag.text if dt_pub_tag else "Data não encontrada"
            
            result = {
                "empresa": keyword, 
                "link": href,
                "titulo": title,
                "descrição": description,
                "dt_pub_noticia": utils.dt_ref_to_isodt(dt_pub),
                "sense_title": utils.get_sentiment_pt(title),
                "sense_description": utils.get_sentiment_pt(description),
                "class_title": utils.get_classify_pt(title),
                "class_description": utils.get_classify_pt(description),
            }
            all_results.append(result)
    return all_results

def main_scrape():
    empresas = ["Komatsu", "Votorantim Cimentos", "Haribo"]
    empresas = input('inserir empresas, exemplo: Microsoft, Ford, XP Investimentos')
    
    empresas = empresas.split(',')
    resultados = []
    num_pages = int(input('inserir quantidade de páginas a serem procuradas'))
    
    for brand in empresas:
        curr_dados = scrape_google_news(brand, num_pages=num_pages)
        resultados.extend(curr_dados)
        
    import json
    with open('analises.json', 'w') as f:
        json.dump(resultados,f,ensure_ascii=False,indent=4)
    
    df = pd.DataFrame(resultados)
    df.to_excel('analises.xlsx', index=False)

main_scrape()