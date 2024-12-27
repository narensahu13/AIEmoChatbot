# emotion_analyzer.py
from transformers import pipeline
import numpy as np

class EmotionAnalyzer:
    def __init__(self):
        self.classifier = pipeline("text-classification", 
                                 model="bhadresh-savani/distilbert-base-uncased-emotion",
                                 return_all_scores=True)
        self.emotions = ["joy", "sadness", "anger", "fear", "love", "surprise"]
    
    def analyze_emotion(self, text):
        results = self.classifier(text)[0]
        emotions_dict = {item['label']: item['score'] for item in results}
        return emotions_dict
    
    def get_dominant_emotion(self, text):
        emotions = self.analyze_emotion(text)
        return max(emotions.items(), key=lambda x: x[1])