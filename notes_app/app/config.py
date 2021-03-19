class Base(object):
    HOME_URL = "//kishmakov.ru/"
    STATIC_URL = "//kishmakov.ru/static/"


class Dev(Base):
    DEBUG = True
    NOTES_URL = "//127.0.0.1:5003/"


class Prod(Base):
    DEBUG = False
    NOTES_URL = "//kishmakov.ru/notes/"

