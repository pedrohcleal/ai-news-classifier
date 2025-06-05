# 📰 Google News Scraper com Análise de Sentimento e Classificação de Tópicos

Este projeto realiza scraping de notícias do **Google News** com base em palavras-chave (nomes de empresas), aplicando **análise de sentimento** e **classificação temática** usando modelos da Hugging Face. O resultado é exportado em JSON e Excel.

---

## 📌 Funcionalidades

- Scraping de notícias do Google News por empresa.
- Extração de:
  - Título
  - Descrição
  - Data da publicação
  - Link da notícia
- Tradução automática PT ↔️ EN.
- Análise de **sentimento** do título e da descrição.
- **Classificação temática** das notícias.
- Exportação dos resultados para:
  - `analises.json`
  - `analises.xlsx`

---

## 🗂 Estrutura

```

src/
├── config/
│   ├── scraper\_configs.py          # Configurações de scraping com retry
│   └── transformers\_config.py      # Pipelines de NLP (sentimento e classificação)
├── utils/
│   └── utils.py                    # Funções auxiliares (tradução, NLP, datas)
├── main.py                         # Script principal

````

---

## ⚙️ Requisitos

- Python 3.10+
- [cloudscraper](https://pypi.org/project/cloudscraper/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [transformers](https://pypi.org/project/transformers/)
- [dateparser](https://pypi.org/project/dateparser/)

### Instalação dos pacotes

```bash
pip install -r requirements.txt
````

---

## 🚀 Como usar

```bash
cd src
python main.py
```

O script irá:

1. Buscar notícias das empresas: **Komatsu**, **Votorantim Cimentos**, **Haribo**.
2. Processar cada título e descrição com análise de sentimento e classificação.
3. Salvar os resultados em:

   * `analises.json`
   * `analises.xlsx`

---

## 🧠 Modelos utilizados

| Tarefa                | Modelo HuggingFace                                                                                                            |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Classificação         | [`classla/multilingual-IPTC-news-topic-classifier`](https://huggingface.co/classla/multilingual-IPTC-news-topic-classifier)   |
| Análise de Sentimento | [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) |

---

## 📊 Exemplo de saída

```json
{
  "empresa": "Haribo",
  "link": "https://example.com",
  "titulo": "Haribo anuncia nova fábrica no Brasil",
  "descrição": "Empresa alemã investe em expansão no mercado latino-americano.",
  "dt_pub_noticia": "2025-06-05",
  "sense_title": 4,
  "sense_description": 5,
  "class_title": "Negócios",
  "class_description": "Economia"
}
```

---

## 🛡️ Aviso legal

O scraping do Google News é feito apenas para fins educacionais. Utilize com responsabilidade e evite sobrecarregar os servidores.

---