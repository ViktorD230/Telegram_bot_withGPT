import telebot
import openai
import json


telegram_key = '6257906376:AAG5UxtIWM8oJMg7FW8h9_0buIFj7hMzWWU'
openai.api_key = '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'

bot = telebot.TeleBot(telegram_key)
chat_history = []


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет, я GPT бот. Готов тебе помочь')


@bot.message_handler(content_types=['text'])
def main(message):
    reply = ""
    response = openai.Completion.create(
        prompt=message.text,
        engine='gpt-3.5-turbo',
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15
    )

    if response and response.choices:
        reply = response.choices[0].text.strip()

    else:
        reply = 'Ой, что то не так'

    chat_history.append({
        'user_message': message.text,
        'bot_reply': reply})

    bot.send_message(message.chat.id, reply)

    save_chat_history()

def save_chat_history():
    with open('chat_history.json', 'w') as file:
        json.dump(chat_history, file)


bot.polling(none_stop=True)
