import telebot
from telebot import types

token = open('C:/Secret/token_Rin_bot.txt','r')
id_Dev = open('C:/Secret/id_Dev.txt','r')
id_Admin = open('C:/Secret/id_Admin.txt','r')
id_Chanel = -1001874898194
user_info = []

bot = telebot.TeleBot(token.read())

vacancies = ['1.Старший специалист HR','2.Младший специалист HR','3. Администратор  в международную  школы', 
            '4.Преподаватель математики в начальной школе/математики и физики в средней школе',
            '5.Воспитатель (Теам teacher)', 
            '6.Преподаватель математики начальной школы']

@bot.message_handler(commands=['start','help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in vacancies:
        markup.add(types.KeyboardButton(i))

    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>. ' \
           f' мы рады ,что вы выбрали нашу компанию! Выберите направление...' 
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def func(message):
    global user_info
    if(message.text in vacancies):
        temp = bot.send_message(message.chat.id, text=f'Загрузите свое резюме по направлению {message.text} ')
        user_info = [f'@{message.from_user.username}', message.from_user.first_name, message.from_user.last_name,'\n', message.text]
        bot.register_next_step_handler(temp, forward)

@bot.message_handler(content_types=['text'])
def forward(message):
    if (message.text in vacancies):
        func(message)
    elif(message.document):
        bot.send_message(id_Chanel, ' '.join(user_info))
        bot.send_document(id_Chanel, message.document.file_id)
        bot.send_message(message.chat.id, 'Благодарим за проявленный интерес. Специалист рассмотрит ваше резюме и обязательно свяжется с вами!')
        

bot.polling(none_stop=True)
