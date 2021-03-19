class Base(object):
    HOME_URL = "http://kishmakov.ru/"
    STATIC_URL = "http://kishmakov.ru/static/"
    GITHUB_EDIT_URL = "https://github.com/kishmakov/myweb/edit/master/notes_app/notes/"


class Dev(Base):
    DEBUG = True
    NOTES_URL = "http://127.0.0.1:5003/"


class Prod(Base):
    DEBUG = False
    NOTES_URL = "http://kishmakov.ru/notes/"

