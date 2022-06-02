from telebot import *
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('9ed0cd9b41889990de175ca31bdf8e0d', config_dict)  # Weather API
bot = telebot.TeleBot('5103126599:AAH_l0db3nSU1IvAZ2aImrSsgi6AZsA6ELg')
BOT_URL = 'https://telegabryansk.herokuapp.com/'


@bot.message_handler(commands=['weather'])
def weather(message):
    place = bot.send_message(message.chat.id, 'Какой город вас интересует?', parse_mode='html')
    bot.register_next_step_handler(place, weather_1)


def weather_1(message):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    # Статус
    status = observation.weather.detailed_status
    # Температура
    temp = observation.weather.temperature('celsius')
    t1 = temp["temp"]
    t2 = temp["feels_like"]
    t3 = temp["temp_max"]
    t4 = temp["temp_min"]
    # Скоросить ветра
    wind = observation.weather.wind()['speed']
    # Влажность
    humi = observation.weather.humidity
    # Время
    time = observation.weather.reference_time('iso')
    # Давление
    pr = observation.weather.pressure['press']
    # Видимость
    vd = observation.weather.visibility_distance
    bot.send_message(message.chat.id,
                     f'Температура в городе {message.text.capitalize()} составляет {round(t1, 1)}°С, ощущается как {round(t2, 1)}°С. '
                     f'Максимальная температура сегодняшнего дня составит {round(t3, 1)}°С, минимальная {round(t4, 1)}°С.\n'
                     f'Cкорость ветра на данный момент {wind} м/с, влажность {humi} %, давление {round(pr * 0.750064)} мм.рт.ст., видимость {round(vd / 1000, 1)} км.\n'
                     f'Последнее обновление {time}. Общий статус: {status}', parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'<b>Привет, <u>{message.from_user.first_name}</u>.</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['mylocation'])
def location(message):
    bot.send_message(message.chat.id, "<b>Ищу тебя!</b>", parse_mode='html')
    bot.send_location(message.chat.id, 53.2521, 34.3717)


@bot.message_handler(commands=['web'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("YouTube", url="https://www.youtube.com/"))
    markup.add(types.InlineKeyboardButton("Google", url="https://www.google.ru/webhp?hl=ru/"))
    markup.add(types.InlineKeyboardButton("VK", url="https://vk.com/"))

    bot.send_message(message.chat.id, "<b>Список сайтов: </b>", parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    website = types.KeyboardButton('/web')
    start = types.KeyboardButton('/start')
    location = types.KeyboardButton('/mylocation')
    id = types.KeyboardButton('id')
    photo = types.KeyboardButton('photo')
    video = types.KeyboardButton('video')
    audio = types.KeyboardButton('audio')
    weather = types.KeyboardButton('/weather')
    markup.add(website, start, location, id, photo, video, audio, weather)
    bot.send_message(message.chat.id, "<b>Список возможностей: </b>", parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, "<b>Классная пикча!</b>", parse_mode='html')


@bot.message_handler(content_types=['audio'])
def get_user_photo(message):
    bot.send_message(message.chat.id, "<b>Dolbit NORMAL`NO</b>", parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    if message.text.lower() in ['ку', 'привет', 'здарова']:
        bot.send_message(message.chat.id, "<b>И тебе привет</b>", parse_mode='html')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f"<b>Твой ID:</b> {message.from_user.id}", parse_mode='html')
    elif message.text.lower() == 'photo':
        photo = open('1.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text.lower() == 'video':
        video = open('Три кота phonk.mp4', 'rb')
        bot.send_message(message.chat.id, "<b>Загружаю видос, это не так просто...</b>", parse_mode='html')
        bot.send_video(message.chat.id, video)
    elif message.text.lower() == 'audio':
        audio = open('Бустеренко.mp3', 'rb')
        bot.send_message(message.chat.id, "<b>Делаю Трек за 5 секунд...</b>", parse_mode='html')
        bot.send_audio(message.chat.id, audio)
    else:
        bot.send_message(message.chat.id,
                         "<b>Если хочешь со мной взаимодействовать, узнай список моих возможностей (/help)</b>",
                         parse_mode='html')


bot.polling(none_stop=True)
