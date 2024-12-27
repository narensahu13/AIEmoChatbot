import streamlit as st
from config import Config
from emotion_analyzer import EmotionAnalyzer
from conversation_memory import ConversationMemory
from chatbot import EmotionalChatbot
import emoji

def init_session_state():
    if 'chatbot' not in st.session_state:
        config = Config()
        emotion_analyzer = EmotionAnalyzer()
        memory = ConversationMemory()
        st.session_state.chatbot = EmotionalChatbot(config, emotion_analyzer, memory)

def get_emotion_emoji(emotion):
    emoji_map = {
        "joy": "😊",
        "sadness": "😢",
        "anger": "😠",
        "fear": "😨",
        "love": "🥰",
        "surprise": "😲"
    }
    return emoji_map.get(emotion, "😐")

def main():
    st.title("Emotional Chatbot Friend")
    st.write("Chat with your AI friend who understands and responds to emotions!")
    
    init_session_state()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(f"{message['content']} {get_emotion_emoji(message['emotion'])}")
    
    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "emotion": "neutral"})
        
        # Get chatbot response
        response, emotion = st.session_state.chatbot.generate_response(prompt)
        
        # Add assistant response to chat history
        dominant_emotion = max(emotion.items(), key=lambda x: x[1])[0]
        st.session_state.messages.append({"role": "assistant", "content": response, "emotion": dominant_emotion})
        
        # Force streamlit to rerun and update the chat
        st.rerun()

if __name__ == "__main__":
    main()