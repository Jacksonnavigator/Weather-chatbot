import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import os
import requests

# Set your OpenWeatherMap API key here
os.environ['OPENWEATHERMAP_API_KEY'] = 'e205be3d0629e90f431219113346fd12'

# Function to retrieve weather information
def get_weather(country, city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        return "API key not found. Please set the OPENWEATHERMAP_API_KEY environment variable."

    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}'
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching weather data: {e}"

    data = response.json()

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return f"The weather in {city}, {country} is {weather_description}. Temperature: {temperature:.2f}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s."
    else:
        return f"Sorry, I couldn't retrieve the weather information for {city}, {country}."

# Define pattern-response pairs for the chatbot
pairs = [
    [
        r"hi|hello",
        ["Hello", "Hi", "Hey"]
    ],
    [
        r"how are you ?",
        ["I'm good, thank you", "I'm doing well"]
    ],
    [
        r"what is your name ?",
        ["My name is ChatBot", "You can call me ChatBot"]
    ],
    [
        r"what is the weather",
        ["Sure, I can help you with that. Please provide the recipient location by country and city."]
    ],
    [
        r"(.*) weather in (.*)",
        [lambda country, city: get_weather(city, country)]
    ],
    [
        r"bye",
        ["Goodbye", "Bye", "See you later"]
    ]
]

# Define the chatbot function
def chat_bot(input_message):
    chat = Chat(pairs, reflections)
    response = chat.respond(input_message)
    return response

# Streamlit web application
def main():
    st.title("ChatBot with Weather Integration")

    st.sidebar.title("Chat")

    user_input = st.text_input("You:")
    if st.button("Send"):
        if user_input.strip() == "":
            st.write("Please enter a message.")
        else:
            st.write("ChatBot:", chat_bot(user_input))

if __name__ == "__main__":
    main()
