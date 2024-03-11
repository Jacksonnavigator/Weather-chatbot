import nltk
from nltk.chat.util import Chat, reflections
import os
import requests

# Set your OpenWeatherMap API key here
os.environ['OPENWEATHERMAP_API_KEY'] = 'your_actual_api_key'

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
        temperature_celsius = temperature - 273.15
        return f"The weather in {city}, {country} is {weather_description} with a temperature of {temperature_celsius:.2f} degrees Celsius."
    else:
        return "Sorry, I couldn't retrieve the weather information for that location."

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
        r"what is the weather in (.*)\?",
        [get_weather("\\1", "\\2")]
    ],
    [
        r"bye",
        ["Goodbye", "Bye", "See you later"]
    ]
]

# Define the chatbot function
def chat_bot():
    print("Hi, I'm ChatBot. How can I help you today?")
    chat = Chat(pairs, reflections)
    while True:
        user_input = input("You: ")
        response = chat.respond(user_input)
        print("ChatBot:", response)
        if user_input.lower() == 'exit':
            break

# Main function to start the chatbot
if __name__ == "__main__":
    chat_bot()
