from deep_translator import GoogleTranslator
from textblob import TextBlob
from config.transformers_config import get_classifier_news_ia, get_sentiment_news_ia
from models.textblob_tags import pos_tags

news_classifier = get_classifier_news_ia()
news_sentiment = get_sentiment_news_ia()


def translate_pt_to_en(txt: str):
    traducao = GoogleTranslator(source='pt', target='en').translate(txt)
    return traducao

def translate_en_to_pt(txt: str):
    traducao = GoogleTranslator(source='en', target='pt').translate(txt)
    return traducao


# def get_sentiment_pt(txt_pt: str) -> tuple:
#     txt_en = translate_pt_to_en(txt_pt)
    
#     blob = TextBlob(txt_en)
#     polaridade = blob.sentiment.polarity
#     subjetividade = blob.sentiment.subjectivity
    
#     if polaridade > 0.3:
#         sense = "Positivo"
#     elif polaridade < -0.3:
#         sense = "Negativo"
#     else:
#         sense = "Neutro"

#     if subjetividade >= 0.6:
#         subj_type = "Subjetivo"
#     elif subjetividade <= 0.4:
#         subj_type = "Objetivo"
#     else:
#         subj_type = "Moderado"
    
#     return (sense, subj_type)

def get_sentiment_pt(txt_pt):
    txt_en = translate_pt_to_en(txt_pt)
    result = news_sentiment(txt_en)
    starts: str = result[0]['label']
    n_starts = int(starts.split(' ')[0])
        
    print(f'Sense: {n_starts}')
    return n_starts

def get_classify_pt(txt_pt):
    txt_en = translate_pt_to_en(txt_pt)
    resultado = news_classifier(txt_en)
    print(f'class = {resultado[0]["label"]}')
    return translate_en_to_pt(resultado[0]["label"])


def get_tags_pt(txt_pt: str):
    txt_en = translate_pt_to_en(txt_pt)
    
    wiki = TextBlob(txt_en)
    resultado = []
    for palavra, tag in list(wiki.tags):
        descricao = pos_tags.get(tag, 'Tag desconhecida')
        resultado.append((translate_en_to_pt(palavra), tag, descricao))
    return resultado