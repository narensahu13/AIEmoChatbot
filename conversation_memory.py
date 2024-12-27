from dataclasses import dataclass
from typing import List, Dict
import datetime

@dataclass
class Message:
    text: str
    sender: str
    timestamp: datetime.datetime
    emotion: Dict[str, float]

class ConversationMemory:
    def __init__(self, max_history=10):
        self.history: List[Message] = []
        self.max_history = max_history
        
    def add_message(self, text: str, sender: str, emotion: Dict[str, float]):
        message = Message(
            text=text,
            sender=sender,
            timestamp=datetime.datetime.now(),
            emotion=emotion
        )
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_emotional_context(self) -> Dict[str, float]:
        if not self.history:
            return {}
        
        emotions = {"joy": 0, "sadness": 0, "anger": 0, "fear": 0, "love": 0, "surprise": 0}
        for message in self.history:
            for emotion, score in message.emotion.items():
                emotions[emotion] += score
        
        # Normalize
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions