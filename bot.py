import telebot
from config import bot_token
from rm_connector import RedmineConnector

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, ''' Для создания задачи отправь мне сообщение в формате:

#ошибка {Тема задачи}
Описание задачи

Поддерживаемые хештеги: #ошибка, #улучшение, #поддержка
''')


@bot.message_handler(content_types=['text'])
def issue_message(message):
    text = message.text.lower()
    if '#ошибка' in text:
        subject = text.replace('#ошибка', '')
        tracker_id = 1
    elif '#улучшение' in text:
        subject = text.replace('#улучшение', '')
        tracker_id = 2
    elif '#поддержка' in text:
        subject = text.replace('#поддержка', '')
        tracker_id = 3
    rm = RedmineConnector()
    task_subject = subject.split('\n')[0]
    task_description = subject.replace(task_subject, '')

    issue_number = rm.create_issue(tracker_id=tracker_id, task_subject=task_subject, task_description=task_description, telegram_id=message.chat.id)
    bot.send_message(message.chat.id, f'Задача {issue_number} создана')



bot.polling()


