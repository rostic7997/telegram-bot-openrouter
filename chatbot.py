import telebot
import os
import requests

# Replace with your actual tokens
TELEGRAM_TOKEN = 'создай бота в telegram'
OPENROUTE_API_KEY = 'https://openrouter.ai/'
MODEL_NAME = "mistralai/mistral-small-3.1-24b-instruct:free"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_ai_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENROUTE_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': MODEL_NAME,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    try:
        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return "Виникла помилка при обробці запиту до AI."
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing AI response: {e}")
        return "Отримано некоректну відповідь від AI."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я AI бот. Задай мені будь-яке питання.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    ai_response = get_ai_response(message.text)
    bot.reply_to(message, ai_response)

if __name__ == '__main__':
    try:
        print("Бот запускається...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Виникла помилка під час запуску або роботи бота: {e}")
    else:
        print("Бот успішно запущено!")