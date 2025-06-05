from textblob import TextBlob
from deep_translator import GoogleTranslator

texto = "Several people reported feeling dizzy and unwell after eating from a 1kg pack of Haribo Happy Cola F!ZZ"

traducao = GoogleTranslator(source='pt', target='en').translate(texto)
print(traducao)
wiki = TextBlob(traducao)

print(wiki.tags)
print(wiki.noun_phrases)
print(wiki.sentiment)
print(wiki.sentiment_assessments)