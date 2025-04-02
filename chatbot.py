import streamlit as st
import ollama
import json
import requests
import nltk
from utils.helpers import analyze_sentiment, search_wikipedia

# Ensure required NLTK resources are downloaded
nltk.download('wordnet', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Load API keys
with open("config.json") as config_file:
    config = json.load(config_file)

# Weather API Function
def get_weather(city="New York"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config['weather_api_key']}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != 200:
        return "Sorry, I couldn't fetch the weather."
    return f"🌡️ Temperature: {data['main']['temp']}°C, {data['weather'][0]['description']}"

# News API Function
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={config['news_api_key']}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    if not articles:
        return "No news available."
    news_list = [f"📰 {article['title']} - {article['source']['name']}" for article in articles[:5]]
    return "\n".join(news_list)

# Chatbot Response
def get_chatbot_response(user_input):
    if "weather" in user_input:
        return get_weather()
    elif "news" in user_input:
        return get_news()
    elif "who is" in user_input or "what is" in user_input:
        return search_wikipedia(user_input.replace("who is ", "").replace("what is ", ""))
    
    # Use LLaMA 2 for general responses
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": user_input}])
    return response["message"]["content"]

# Streamlit UI
st.set_page_config(page_title="Advanced AI Chatbot", page_icon="🦙", layout="wide")
st.title("🦙 Advanced AI Chatbot (LLaMA 2)")
st.write("🔹 **Features**: AI Chat, Weather, News, Wikipedia, Sentiment Analysis.")

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
with st.container():
    for message in st.session_state.chat_history:
        role, text = message
        st.chat_message(role).write(text)

# User Input
user_input = st.chat_input("Type your message...")
if user_input:
    with st.spinner("Processing..."):
        sentiment = analyze_sentiment(user_input)
        response = get_chatbot_response(user_input)

    # Display Messages
    st.chat_message("user").write(f"({sentiment}) {user_input}")
    st.chat_message("assistant").write(response)

    # Save to Chat History
    st.session_state.chat_history.append(("user", f"({sentiment}) {user_input}"))
    st.session_state.chat_history.append(("assistant", response))
