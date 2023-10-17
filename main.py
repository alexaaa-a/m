import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6647321004:AAEEdsPY9cdGZS5_VkjN6SegPjJUEs7zqws",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация"  # Можно менять текст
text_button_1 = "Подготовка к ОГЭ"  # Можно менять текст
text_button_2 = "Подготовка к ЕГЭ"  # Можно менять текст
text_button_3 = "Как стать Python разработчиком за 3 дня?"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Приветствуем нового обучающегося Умскул, рады видеть тебя в рядах наших учеников! Для выбора курса пройди первичную регистрацию',
        # Ламповое приветствие
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id,
                     'Отлично! Ваше *имя на кириллице*')  # Проверку вводить не стал, т.к. нет коннекта с БД
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id,
                     'Супер! [Укажите ваш возраст в этом опроснике и продублируйте здесь](https://forms.gle/E2La47mTPZJnQdNk6)')  # Таблица рабочая, буду рад увидеть вас в ней)
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию!', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, 'Мы вас ждем!(https://vk.com/umschoolofficial)')


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, 'Скорее записаться на первое занятие!(https://vk.com/umschoolofficial)')


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, 'Начинаем карьерный путь вместе с Умскул!(https://vk.com/umschoolofficial)')


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()