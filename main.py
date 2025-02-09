import telebot

import base64
from PIL import Image
from io import BytesIO

from logic_ai import Text2ImageAPI

from config import bot_api, ai_api, ai_secret

def generate_img(text):
	api = Text2ImageAPI('https://api-key.fusionbrain.ai/', ai_api, ai_secret)
	model_id = api.get_model()
	uuid = api.generate(text, model_id)
	images = api.check_generation(uuid)[0]

    # Строка Base64, представляющая изображение
	base64_string = images  # здесь должна быть ваша строка Base64

    # Декодируем строку Base64 в бинарные данные
	decoded_data = base64.b64decode(base64_string)

    # Создаем объект изображения с помощью PIL
	image = Image.open(BytesIO(decoded_data))

    # Отображаем изображение (опционально)
	return image

bot = telebot.TeleBot(token=bot_api)

@bot.message_handler(commands=['start'])
def hello(msg):
	bot.send_message(msg.chat.id, "Привет, я бот с ИИ для генерации изображений! Чтобы сгенерировать изображение по запросу, напиши /img")

@bot.message_handler(commands=['img'])
def get_text(msg):
	text = bot.send_message(msg.chat.id, 'Напиши свой запрос')
	bot.register_next_step_handler(text, generate)

def generate(msg):
	bot.send_message(msg.chat.id, 'Генерирую...')
	image = generate_img(text=msg.text)
	bot.send_photo(msg.chat.id, photo=image)

if __name__ == "__main__":
	bot.polling(none_stop=True)