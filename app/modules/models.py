from starlette.requests import empty_receive


class Coffee:
    def __init__(self,name, description,id=None):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return "{}".format(self.id)


class Machine:
    def __init__(self, state, type, id = None, name=None):
        self.id = id
        self.name = name
        self.state = state
        self.type = type


class Preparation:
    def __init__(self, coffee, creation_date, last_update, machine, id, saved, state, next_time):
        self.coffee = coffee
        self.creation_date = creation_date
        self.last_update = last_update
        self.machine = machine
        self.id = id
        self.saved = saved
        self.state = state
        self.next_time = next_time


class PreparationSaved(Preparation):

    def __init__(self, coffee, creation_date, last_update, machine, id, saved, state, next_time, name, days_of_week, hours, last_time):
        super().__init__(coffee, creation_date, last_update, machine, id, saved, state, next_time)
        self.days_of_week = days_of_week
        self.next_time = next_time
        self.hours = hours
        self.last_time = last_time
        self.name = name