from main import get_data

import telebot

with open('token.txt', 'r') as file:
    TOKKEN = file.readline()

bot = telebot.TeleBot(TOKKEN)

all_categories = {
    '/tabacco': ' - для просмотра ассортимента *табака*',
    '/hookah': ' - для просмотра *кальянов*',
    '/mouthpiece': ' - для просмотра *мундштуков*',
    '/couple': ' - для просмотра *чаш* для кальянов',
    '/flask': ' - для просмотра *колб* для кальянов',
    '/electrosig': ' - для просмотра ассортимента *Электронных сигарет*',
    '/coal': ' - для просмотра ассортимента *угля*',
    '/accessories': ' - для просмотра ассортимента *аксессуаров*',
    '/forceps': ' - для просмотра ассортимента *шипцов*',
    '/awl': ' - для просмотра ассортимента *шил и шиловилок*',
    '/clean': ' - для просмотра *средств для чистки кальяна*',
    '/hose': ' - для просмотра ассортимента *шлангов*',
    '/warm': ' - для просмотра аксессуаров для *разогрева кальяна*',
    '/notabacco' : ' - для просмотра *бестабачных смесей*',
    '/pods' : ' - для просмотра *подов* для парения'
}


@bot.message_handler(commands=['start', 'menu'])
def get_start(message):
    msg = ''
    for command, text in all_categories.items():
        msg += command + text + '\n'
    bot.send_message(
        message.chat.id, 'Чтобы посмотреть ассортимент магазина, выберите одну из следующих категорий')
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(commands=['electrosig'])
def choose_type(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    hqd = telebot.types.KeyboardButton('/HQD')
    gip_pro = telebot.types.KeyboardButton('/GipPro')
    markup.add(hqd, gip_pro)
    bot.send_message(
        message.chat.id, 'Выберите марку электронной сигареты', reply_markup=markup)


@bot.message_handler(commands=['GipPro'])
def send_gippro_list(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    butt_800 = telebot.types.KeyboardButton('800')
    butt_1600 = telebot.types.KeyboardButton('1600')
    markup.add(butt_800, butt_1600)
    msg = bot.send_message(
        message.chat.id, 'Выберите кол-во затяжек', reply_markup=markup)
    bot.register_next_step_handler(msg, choose_category, 'GipPro')


@bot.message_handler(commands=['HQD'])
def send_hqd_list(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    butt_1200 = telebot.types.KeyboardButton('1200')
    butt_1600 = telebot.types.KeyboardButton('1600')
    butt_2000 = telebot.types.KeyboardButton('2000')
    butt_2500 = telebot.types.KeyboardButton('2500')
    markup.add(butt_1200, butt_1600, butt_2000, butt_2500)
    msg = bot.send_message(
        message.chat.id, 'Выберите кол-во затяжек', reply_markup=markup)
    bot.register_next_step_handler(msg, choose_category, 'HQD')


def choose_category(message, sig_type):
    list_of_products = get_data(sig_type + ' ' + message.text)
    bot.send_message(message.chat.id, '\n'.join(list_of_products))
    bot.send_message(message.chat.id, 'для возврата в меню, нажмите -> /menu' )


@bot.message_handler(commands=['tabacco'])
def select_tabacco_type(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=1, one_time_keyboard=True)
    butt_ez = telebot.types.KeyboardButton('Легкий')
    butt_md = telebot.types.KeyboardButton('Средний')
    butt_st = telebot.types.KeyboardButton('Крепкий')
    markup.add(butt_st, butt_md, butt_ez)
    msg = bot.send_message(
        message.chat.id, 'Выберите крепость табака', reply_markup=markup)
    bot.register_next_step_handler(msg, get_tabacco_by_type)


def get_tabacco_by_type(message):
    tabacco_categories = {
        'Легкий': ['Duft Pheromone (25 гр)', 'Daily Hookah 60 грамм', '"Элемент" Воздух 40гр', '"Sebero" Arctic Mix 30гр', 'Икс, 50 г', 'Smoke Angels 25 грамм',
                   'SPECTRUM Classic 40 гр'],
        'Средний': ['Burn BLACK 25 гр', 'MustHave 25 грамм', 'VENOM Medium 25 грамм', 'Pure 20 гр', 'Original Virginia 25 грамм Med.', 'Duft  (25 гр)',
                    '"Элемент" Вода 40гр', 'DarkSide CORE 30 грамм', 'Северный 40 гр', 'SPECTRUM Hard Line 40 гр', 'Мэтт Пир 50 гр', 'Сарма 40гр', '"Sebero"  40 гр.',
                    'DarkSide SHOT 30 грамм', '"Элемент" M 25гр', '"Элемент" Вода 40гр', 'Северный MIX 100 гр', 'VENOM Medium 25 грамм', '"Sebero"  30 гр. Limited',
                    'DarkSide 100 грамм', 'MustHave 100гр', 'Душа'],
        'Крепкий': ['Satyr 25 гр', 'BONCHE(сигарный) 30 грамм', 'VENOM HARD 25 грамм', 'BONCHE(сигарный) 30 грамм', 'НАШ 40гр', 'VENOM MIX 40 грамм', '"Элемент" Земля 40гр', 'Satyr 25 гр',
                    'Satyr 100 гр']
    }
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, one_time_keyboard=True)
    for elem in tabacco_categories[message.text]:
        butt = telebot.types.KeyboardButton(elem)
        markup.add(butt)
    msg = bot.send_message(
        message.chat.id, 'Выберите марку табака', reply_markup=markup)
    bot.register_next_step_handler(msg, select_tabacco)


def select_tabacco(message):
    tabacco_list = get_data(message.text)
    bot.send_message(message.chat.id, '\n'.join(tabacco_list))
    bot.send_message(message.chat.id, 'для возврата в меню, нажмите -> /menu' )

@bot.message_handler(commands=['notabacco'])
def chose_notabacco(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    brusko_50 = telebot.types.KeyboardButton('BRUSKO, 50 г')
    brusko_20 = telebot.types.KeyboardButton('BRUSKO BIT, 20 г')
    chabacco = telebot.types.KeyboardButton('Chabacco')
    markup.add(brusko_50, brusko_20, chabacco)
    msg = bot.send_message(message.chat.id, 'Выберите марку бестабачной смеси', reply_markup=markup)
    bot.register_next_step_handler(msg, send_notabacco)
    

def send_notabacco(message):
    notabacco = get_data(message.text)
    bot.send_message(message.chat.id, '\n'.join(notabacco))
    bot.send_message(message.chat.id, 'для возврата в меню, нажмите -> /menu' )


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text in all_categories:
        pr_list = check_category(message.text)
        bot.send_message(message.chat.id, '\n'.join(pr_list))
        bot.send_message(message.chat.id, 'для возврата в меню, нажмите -> /menu' )
    else:
        with open('answer.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)


def check_category(command):
    data = {
        '/hookah': 'Кальяны',
        '/mouthpiece': 'Мундштуки',
        '/couple': 'Чаши',
        '/flask': 'Колбы',
        '/coal': 'Уголь',
        '/accessories': 'Аксессуары',
        '/forceps': 'Щипци',
        '/awl': 'Шило и шило-вилки',
        '/clean': 'Средства для чистки кальяна',
        '/hose': 'Шланги',
        '/warm': 'Для разогрева кальяна',
        '/pods' : 'Многоразки',
    }
    list_of_products = get_data(data[command])
    return list_of_products


bot.polling(non_stop=True, interval=0)
