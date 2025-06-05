from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


def get_classifier_news_ia():
    model_name = "classla/multilingual-IPTC-news-topic-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return classifier

def get_sentiment_news_ia():
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return classifier
