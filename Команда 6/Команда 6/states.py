from aiogram.dispatcher.filters.state import StatesGroup, State


class Menu(StatesGroup):
    menu = State()

    event = State()
    user_event = State()
    filter_event = State()
    category_event = State()
    date_event = State()
    distance_event = State()

    my_event = State()
    my_event_create = State()
    description = State()
    time = State()
    loc = State()
    category = State()


    back_call = State()

class NewEvent(StatesGroup):
    loc = State()
    description = State()

