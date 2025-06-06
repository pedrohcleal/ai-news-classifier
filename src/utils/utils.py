from deep_translator import GoogleTranslator
from config.transformers_config import get_classifier_news_ia, get_sentiment_news_ia
import dateparser
from datetime import datetime


news_classifier = get_classifier_news_ia()
news_sentiment = get_sentiment_news_ia()

def translate_pt_to_en(txt: str):
    traducao = GoogleTranslator(source='pt', target='en').translate(txt)
    return traducao

def translate_en_to_pt(txt: str):
    traducao = GoogleTranslator(source='en', target='pt').translate(txt)
    return traducao

def get_sentiment_pt(txt_pt):
    txt_en = translate_pt_to_en(txt_pt)
    result = news_sentiment(txt_en)
    starts: str = result[0]['label']
    n_starts = int(starts.split(' ')[0])
    return n_starts

def get_classify_pt(txt_pt):
    txt_en = translate_pt_to_en(txt_pt)
    resultado = news_classifier(txt_en)
    return translate_en_to_pt(resultado[0]["label"])


def dt_ref_to_isodt(txt_dt):
    data_referencia = datetime.now()

    data = dateparser.parse(
        txt_dt,
        languages=['pt'],
        settings={'RELATIVE_BASE': data_referencia}
    )

    if data:
        return data.date().isoformat()
    else:
        return '0000-00-00'