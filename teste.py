from textblob import TextBlob
from deep_translator import GoogleTranslator

texto = "Python é uma linguagem de programação incrível."

traducao = GoogleTranslator(source='pt', target='en').translate(texto)
print(traducao)
wiki = TextBlob(traducao)

print(wiki.tags)
print(wiki.noun_phrases)
print(wiki.sentiment.polarity)
print(wiki.sentiment_assessments)