class Base(object):
    HOME_URL = "http://kishmakov.ru/"
    STATIC_URL = "http://kishmakov.ru/static/"


class Dev(Base):
    DEBUG = True
    NOTES_URL = "http://127.0.0.1:5003/"


class Prod(Base):
    DEBUG = False
    NOTES_URL = "http://kishmakov.ru/notes/"

