from decouple import config

class Config:
    OPENAI_API_KEY = config('OPENAI_API_KEY')
    MAX_HISTORY_LENGTH = 10
    EMOTION_THRESHOLD = 0.5
    DEFAULT_PERSONALITY = "friendly and empathetic"