from pprint import pprint
from bs4 import BeautifulSoup
import time
import pandas as pd
from playwright.sync_api import sync_playwright, Page
from utils import ia_utils, page_utils, utils
from config.scraper_configs import cloud_scraper, HEADERS

    
def scrape_google_news(keyword, page: Page, num_pages=3) -> list[dict]:
    all_results = []

    for pag_n in range(num_pages):
        start = pag_n * 10
        url = f"https://www.google.com/search?q={keyword}&tbm=nws&start={start}"

        response = cloud_scraper.get(url, headers=HEADERS, timeout=90)
        soup = BeautifulSoup(response.text, "html.parser")

        print(f"\n Página {pag_n + 1} - {url}")
        
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
            page_text = page_utils.get_all_txt(href, page)
            
            result = {
                "empresa": keyword, 
                "link": href,
                "titulo": title,
                "descrição": description,
                "dt_pub_noticia": utils.dt_ref_to_isodt(dt_pub),
                "sense_title": ia_utils.get_sentiment_pt(title)[0],
                "sense_description": ia_utils.get_sentiment_pt(description)[0],
                "sense_text_link": ia_utils.get_sentiment_pt(page_text)[0],
                "class_title": ia_utils.get_classify_pt(title),
                "class_description": ia_utils.get_classify_pt(description),
                "class_text_link": ia_utils.get_classify_pt(page_text)
            }
            #pprint(result)
            all_results.append(result)
            #break
        time.sleep(1)
    return all_results

def main_scrape():
    empresas = ["Komatsu", "Votorantim Cimentos", "Haribo"]
    resultados = []
    import json
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        for brand in empresas:
            curr_dados = scrape_google_news(brand, page, num_pages=10)
            resultados.extend(curr_dados)
        browser.close()
    
    with open('analises_2.json', 'w') as f:
        json.dump(resultados,f,ensure_ascii=False,indent=4)
    
    df = pd.DataFrame(resultados)
    df.to_excel('analises_2.xlsx', index=False)

main_scrape()