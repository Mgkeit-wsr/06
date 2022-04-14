from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
import config

async def send_main_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Найти приключение'),
        InlineKeyboardButton('Мои приключения'),
        InlineKeyboardButton('Обратная связь')
    )
    await bot.send_message(chat_id, "Главное меню", reply_markup=markup)


async def send_events_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Показать больше'),
        InlineKeyboardButton('Назад')
    )

    await bot.send_message(chat_id, "Выберите интересное приключение или просмотрите другие!", reply_markup=markup)


async def send_share_location_creator_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        InlineKeyboardButton("Отправить свою локацию", request_location=True),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Круто, где оно будет? Отправь локацию места", reply_markup=markup)


async def send_share_location_finder_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Отправить', request_location=True),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Где будем искать приключение? Отправь свою геолокацию", reply_markup=markup)


async def send_user_events_panel(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Мои планы'),
        InlineKeyboardButton('Организованные приключения'),
        InlineKeyboardButton('Новое приключение'),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Выберите действие", reply_markup=markup)


async def send_finder_type_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Все приключения'),
        InlineKeyboardButton('Приключения по фильтрам'),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Какие приключения интересуют?", reply_markup=markup)


async def send_filter_selection_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('По категории'),
        InlineKeyboardButton('По дате'),
        InlineKeyboardButton('По расстоянию'),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Выберите фильтр", reply_markup=markup)


async def send_categories_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for category in config.CATEGORIES:
        markup.add(InlineKeyboardButton(category))
    markup.add(InlineKeyboardButton('Назад'))
    await bot.send_message(chat_id, "Выберите категорию", reply_markup=markup)


async def send_date_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Сегодня'),
        InlineKeyboardButton('В течение недели'),
        InlineKeyboardButton('В течение месяца'),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Выберите дату", reply_markup=markup)


async def send_distance_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('500 метров'),
        InlineKeyboardButton('2 километра'),
        InlineKeyboardButton('5 километров'),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "В каком радиусе выполнить поиск?", reply_markup=markup)


async def send_report_menu(bot, chat_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(chat_id, "Отправьте сообщение для разработчиков", reply_markup=markup)
