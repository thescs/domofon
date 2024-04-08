import telebot
import time
import subprocess

# Устанавливаем режим работы пинов на выход
subprocess.run(['gpio', '-1', 'mode', '3', 'out'])
subprocess.run(['gpio', '-1', 'write', '3', '1'])


# Замените 'YOUR_TOKEN' на токен вашего бота
TOKEN = ''

# Замените 'ALLOWED_USER_ID' на id пользователя, команды которого будут обрабатываться
ALLOWED_USER_ID = ''

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Функция для отправки единицы на GPIO порт на заданное время
def send_signal(duration=3):
    subprocess.run(['gpio', '-1', 'write', '3', '0'])
    time.sleep(duration)
    subprocess.run(['gpio', '-1', 'write', '3', '1'])
    # Отправка единицы на GPIO порт

# Обработчик команды /df
@bot.message_handler(commands=['df'])
def handle_df(message):
    # Проверка, что команду отправил разрешенный пользователь
    if str(message.from_user.id) == ALLOWED_USER_ID:
        command = message.text.split()
        if len(command) == 1:
            bot.reply_to(message, 'Отключение на 3 секунды')
            send_signal()
        elif len(command) == 2:
            try:
                bot.reply_to(message, F'Отключение на {int(command[1])} секунд')
                duration = int(command[1])
                send_signal(duration)
            except ValueError:
                bot.reply_to(message, 'Пожалуйста, укажите число после /df для указания длительности.')
    else:
        bot.reply_to(message, 'У вас нет прав для выполнения этой команды.')

# Запуск бота
bot.polling()
