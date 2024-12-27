from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import emoji

class EmotionalChatbot:
    def __init__(self, config, emotion_analyzer, conversation_memory):
        self.config = config
        self.emotion_analyzer = emotion_analyzer
        self.memory = conversation_memory
        self.llm = ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            model="gpt-4o-mini",
            temperature=0.7
        )
    
    def generate_response(self, user_input: str) -> str:
        # Analyze user emotion
        user_emotion = self.emotion_analyzer.analyze_emotion(user_input)
        self.memory.add_message(user_input, "user", user_emotion)
        
        # Get emotional context
        emotional_context = self.memory.get_emotional_context()
        
        # Create system message with emotional awareness
        system_prompt = self._create_emotional_prompt(emotional_context)
        
        # Generate response
        messages = [
            SystemMessage(content=system_prompt),
            *self._format_history(),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.generate([messages]).generations[0][0].text
        
        # Analyze bot's emotional response
        bot_emotion = self.emotion_analyzer.analyze_emotion(response)
        self.memory.add_message(response, "bot", bot_emotion)
        
        return response, bot_emotion
    
    def _create_emotional_prompt(self, emotional_context):
        dominant_emotion = max(emotional_context.items(), key=lambda x: x[1])[0]
        
        prompts = {
            "joy": "You are a cheerful and enthusiastic friend, matching the user's positive energy.",
            "sadness": "You are an empathetic and supportive friend, offering comfort and understanding.",
            "anger": "You are a calm and patient friend, helping to defuse tension.",
            "fear": "You are a reassuring and steady friend, providing security and support.",
            "love": "You are a warm and caring friend, reciprocating affection appropriately.",
            "surprise": "You are an engaged and responsive friend, sharing in the user's amazement."
        }
        
        base_prompt = f"""
        You are an emotional chatbot friend who maintains consistent personality traits while adapting to the emotional context of conversations. {prompts.get(dominant_emotion, self.config.DEFAULT_PERSONALITY)}
        
        Current emotional context:
        {', '.join(f'{k}: {v:.2f}' for k, v in emotional_context.items())}
        
        Respond naturally as a friend would, while being mindful of the emotional context. Keep responses concise and conversational.
        """
        
        return base_prompt
    
    def _format_history(self):
        formatted_messages = []
        for message in self.memory.history[:-1]:  # Exclude the most recent message
            if message.sender == "user":
                formatted_messages.append(HumanMessage(content=message.text))
            else:
                formatted_messages.append(AIMessage(content=message.text))
        return formatted_messages
