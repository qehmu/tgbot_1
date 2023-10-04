import telebot
import sqlite3

bot = telebot.TeleBot('6430541813:AAG7nlhRc8QMRZ3JCyhf3MlFSaFNTltvjJ0')
name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('ideveloper.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет, идет регистрация. Напиши свое имя!')
    bot.register_next_step_handler(message, user_name)
def user_name(message):
        global name
        name = message.text.strip()
        bot.send_message(message.chat.id, 'Теперь придумай пароль!')
        bot.register_next_step_handler(message, user_pass)

def user_pass(message):
        password = message.text.strip()
        conn = sqlite3.connect('ideveloper.sql')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
        conn.commit()
        cur.close()
        conn.close()
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
        bot.send_message(message.chat.id, 'Регистрация прошла успешно', reply_markup=markup)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    conn = sqlite3.connect('ideveloper.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя:{el[1]}, Пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)