# sentiment_analysis.py
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text):
        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']
        if compound_score >= 0.05:
            sentiment = 'positivo'
        elif compound_score <= -0.05:
            sentiment = 'negativo'
        else:
            sentiment = 'neutro'
        return sentiment
