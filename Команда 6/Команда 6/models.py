
users = {}
events = {}


class User:

    def __init__(self, user_id):
        self.id = user_id
        self.events = []
        self.main_events = []

    def join_event(self, event):
        self.events.append(event)
        event.users.update(self)

    def show_events(self):
        rez = []
        for event in self.events:
            rez.append(event)
        return rez

    def create_event(self,
                     description="Играем в настолки!\n\nОписание: Посидим в приятной компании и поиграем в разные настольные игры. У меня их много!\n\nДата проведения: 16.04.2022\nВремя проведения: 17:00"
                     , lng: float = None, lat: float = None):
        event = Event(self.id, description, lng, lat)
        events[event.id] = event
        self.main_events.append(event)
        return event


class Event:
    event_id = 0

    def __init__(self, maintainer: int = None, description: str = None, lng: float = None, lat: float = None):
        self.maintainer = maintainer
        self.users = []
        self.description = description
        self.lng = lng
        self.lat = lat
        self.id = Event.event_id
        Event.event_id += 1

    def add_users(self, users):
        self.users.append(users)
        for user in users:
            user.events.append(self)

def create_user(id:int):
    if id not in users:
        user = User(id)
        users[id] = user
        print(id)

