from transformers import pipeline
import wikipedia

sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    return result[0]['label']

def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "I couldn't find anything on that topic."
