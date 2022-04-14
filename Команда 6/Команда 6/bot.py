import logging
import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import config
import database
import geo_utils
import models
import keyboards

from config import admins
from database import read_filtered_events, find_eventMember
from states import Menu
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5360144235:AAHsfe78_1h5iCwVnwBjaFSVK2E0ijg0iK4'

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

user_data = {}


@dp.message_handler(text="Назад", state="*")
async def back(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        current_state = current_state.__str__().split(":")[1]
        print(current_state)
        if current_state == "menu":
            return
        elif current_state == "event" or current_state == "my_event" or current_state == "back_call":
            await keyboards.send_main_menu(bot, message.chat.id)
            await Menu.menu.set()

        elif current_state == "my_event_create" or current_state == "loc" or current_state == "description":
            await keyboards.send_user_events_panel(bot, message.chat.id)
            await Menu.my_event.set()

        elif current_state == "user_event" or current_state == "filter_event":
            await Menu.event.set()
            await keyboards.send_finder_type_menu(bot, message.chat.id)

        elif current_state == "category_event" or current_state == "date_event" or current_state == "distance_event":
            await Menu.filter_event.set()
            await keyboards.send_filter_selection_menu(bot, message.chat.id)

    except:
        await keyboards.send_main_menu(bot, message.chat.id)
        await Menu.menu.set()

@dp.message_handler(text='Организованные приключения', state="*")
async def main_events(message: types.Message):
    event = read_filtered_events(message.from_user.username)
    for a in event:
        await bot.send_message(message.chat.id, f"id:{a[0]}\n{a[1]}\n{a[2]}/{a[7]}\n{a[3]}\n{a[4]}\n Координаты:{a[5]};{a[6]}")



@dp.message_handler(text='Найти приключение', state="*")
async def find_event(message: types.Message):
    await keyboards.send_finder_type_menu(bot, message.chat.id)
    await Menu.event.set()


@dp.message_handler(text='Приключения по фильтрам', state="*")
async def select_filter(message: types.Message):
    await keyboards.send_filter_selection_menu(bot, message.chat.id)
    await Menu.filter_event.set()


@dp.message_handler(text='По категории', state="*")
async def category_filter(message: types.Message):
    await keyboards.send_categories_menu(bot, message.chat.id)
    await Menu.category_event.set()


@dp.message_handler(text='По дате', state="*")
async def date_filter(message: types.Message):
    await keyboards.send_date_menu(bot, message.chat.id)
    await Menu.date_event.set()


@dp.message_handler(text='По расстоянию', state="*")
async def distance_filter(message: types.Message):
    await keyboards.send_distance_menu(bot, message.chat.id)
    await Menu.distance_event.set()


@dp.message_handler(text='Мои приключения', state="*")
async def user_events_panel(message: types.Message):
    user_events_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    user_events_markup.add(
        InlineKeyboardButton('Мои планы'),
        InlineKeyboardButton('Организованные приключения'),
        InlineKeyboardButton('Новое приключение'),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(message.chat.id, "Выберите действие", reply_markup=user_events_markup)
    await Menu.my_event.set()


@dp.message_handler(text='Мои планы', state="*")
async def user_events(message: types.Message):
    event = find_eventMember(message.from_user.username)
    for a in event:
        await bot.send_message(message.chat.id, f"id:{a[0]}\n{a[1]}\n{a[2]}/{a[7]}\n{a[3]}\n{a[4]}\n Координаты:{a[5]};{a[6]}")



@dp.message_handler(text='Все приключения', state="*")
async def our_events(message: types.Message):
    geobtns_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    geobtns_markup.add(
        InlineKeyboardButton('Отправить', request_location=True),
        InlineKeyboardButton('Назад')
    )
    await bot.send_message(message.chat.id, "Где будем искать приключение? Отправь свою геолокацию",
                           reply_markup=geobtns_markup)
    await Menu.user_event.set()


@dp.message_handler(content_types=['location'], state=Menu.user_event)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "Бетатест"
    await message.answer(reply)
    # await show_events(message)
    #
    # mmm = geo_utils.get_near_polygon(lat, lon, 10)
    # r = database.read_filtered_events(minmax_latitude=mmm[0], minmax_longitude=mmm[1], author_id=message.from_user.id)
    # print(r)
    # await Menu.user_event.set()


@dp.message_handler(text='Показать больше', state="*")
async def show_events(message: types.Message):
    for event in models.events:
        await show_test_card(message, models.events[event])

    more_events_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    more_events_markup.add(
        InlineKeyboardButton('Показать больше'),
        InlineKeyboardButton('Назад')
    )

    await message.answer("Выберите интересное приключение или просмотрите другие!", reply_markup=more_events_markup)


async def show_test_card(message, event):
    answer_markup = types.InlineKeyboardMarkup(row_width=3)
    answer_markup.add(
        InlineKeyboardButton('Приду!', callback_data="go"),
        InlineKeyboardButton('Неинтересно', callback_data="skip"),
        InlineKeyboardButton('Жалоба', callback_data="report")
    )

    await message.answer(event.description, reply_markup=answer_markup)


@dp.callback_query_handler(text='go', state="*")
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    await query.answer(f'Вы приняли приглашение!')
    await Menu.menu.set()

    id = int(query.message.text.split("\n")[0].split(":")[1])
    database.insert_eventMember(id, query.from_user.username)

    await bot.send_message(query.from_user.id,
                           "Отлично! Организатор получит уведомление о вашем приходе.\nАдрес проведения: *тут адрес*\nДата проведения: 16.04.2022\nВремя проведения: 17:00")


@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message):
    greet_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    greet_markup.add(
        InlineKeyboardButton('Найти приключение'),
        InlineKeyboardButton('Мои приключения'),
        InlineKeyboardButton('Обратная связь')
    )
    await bot.send_message(message.chat.id, "Главное меню", reply_markup=greet_markup)
    models.create_user(message.from_user.username)
    await Menu.menu.set()


@dp.message_handler(text='Обратная связь', state="*")
async def report(message: types.Message):
    report_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    report_markup.add(
        InlineKeyboardButton('Назад')
    )
    await Menu.back_call.set()
    await message.answer("Отправьте сообщение для разработчиков бота", reply_markup=report_markup)


@dp.message_handler(text="Новое приключение", state="*")
async def new_event(message: types.Message, state: FSMContext):
    event_creator_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    event_creator_markup.add(
        InlineKeyboardButton("Отправить свою локацию", request_location=True),
        InlineKeyboardButton('Назад')
    )
    await message.answer("Круто, где оно будет? Отправь локацию места", reply_markup=event_creator_markup)
    await Menu.loc.set()


@dp.message_handler(content_types=['location'], state=Menu.loc)
async def event_loc(message: types.Message):
    loc = message.location
    await Menu.description.set()
    markupNone = types.ReplyKeyboardRemove()

    user_data[message.chat.id] = {}
    user_data[message.chat.id]["location"] = loc

    await message.answer("Отправьте описание приключения", reply_markup=markupNone)


@dp.message_handler(content_types=not ['location'], state=Menu.loc)
async def event_loc(message: types.Message):
    await message.answer("Неправилый формат")


@dp.message_handler(state=Menu.description)
async def event_description(message: types.Message):
    user_data[message.chat.id]["description"] = message.text
    await bot.send_message(message.chat.id, "Введите дату когда начнется приключение(пример: 01.02.2020)")
    await Menu.time.set()




@dp.message_handler(lambda message: not is_date(message.text), state=Menu.time)
async def event_time(message: types.Message):
    await bot.send_message(message.chat.id, "Неправильный формат, попробуй еще раз")

@dp.message_handler(lambda message: is_date(message.text), state=Menu.time)
async def event_time(message: types.Message):
    try:
        date = list(map(int, message.text.split(".")))
        date.reverse()
        date = datetime.datetime(*date)

        if datetime.datetime.today().month - date.month >= -1 and date.year-datetime.datetime.today().year<= 1:
            user_data[message.chat.id]["date"] = date
            await Menu.category.set()
            await keyboards.send_categories_menu(bot, message.chat.id)

    except:
        await bot.send_message(message.chat.id, "Что-то пошло не так(")
        await Menu.menu.set()
        await keyboards.send_main_menu(bot, message.chat.id)



def is_date(date):
    try:
        date = date.split(".")
        if len(date) == 3 and int(date[0]) <= 31 and int(date[1]) <= 12 and int(date[2]) >= 2022:
            return True
    except:
        return False


@dp.message_handler(state=Menu.category)
async def category_received(message: types.Message):
    if message.text not in config.CATEGORIES:
        await message.answer("Неверная категория. Выберите из списка")
        return
    user_data[message.chat.id]["category"] = message.text
    await bot.send_message(message.chat.id, "Приключение зарегистрировано!")
    await keyboards.send_main_menu(bot, message.chat.id)
    database.insert_event(message.from_user.username, user_data[message.chat.id]["description"].partition(' ')[0], user_data[message.chat.id]["description"], user_data[message.chat.id]["date"], user_data[message.chat.id]["location"].latitude, user_data[message.chat.id]["location"].longitude, message.text)
    await Menu.menu.set()


@dp.message_handler(state=Menu.back_call)
async def back_call(message: types.Message):
    await message.answer("Ваше сообщение отправлено разработчикам")
    for admin_id in admins:
        await bot.send_message(admin_id, "@" + message.from_user.username + " отправил сообщение: " + message.text)
        await Menu.menu.set()
        await keyboards.send_main_menu(bot, message.chat.id)


@dp.message_handler(state="*")
async def show_menu(message: types.Message):
    await send_welcome(message)


@dp.message_handler(state="*", text="/start")
async def show_hello(message: types.Message):
    await message.answer("aa")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
