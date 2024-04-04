from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests

# Create a new instance of a ChatBot
chatbot = ChatBot('WeatherBot')

# Create a new trainer for the ChatBot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the ChatBot based on the english corpus
trainer.train('chatterbot.corpus.english')

# Function to fetch weather information
def get_weather(city):
    api_key = 'e205be3d0629e90f431219113346fd12'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_info = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity']
        }
        return weather_info
    else:
        return None

# Function to handle user input
def handle_input(user_input):
    if 'weather' in user_input.lower():
        city = input("Please enter the city name: ")
        weather_info = get_weather(city)
        if weather_info:
            response = f"The weather in {city} is {weather_info['description']} with a temperature of {weather_info['temperature']}°C and humidity of {weather_info['humidity']}%."
        else:
            response = "Sorry, I couldn't fetch the weather information for that city."
    else:
        response = chatbot.get_response(user_input)
    return response

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = handle_input(user_input)
    print("Bot:", response)
