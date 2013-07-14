notes_db_name = 'notes'

class NotesRouter(object):
    """Controls access to notes.sqlite"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'notes':
            return notes_db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'notes':
            return notes_db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"

        if obj1._meta.app_label == 'notes' or obj2._meta.app_label == 'notes':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the notes app only appears on the 'notes' db"

        if db == notes_db_name:
            return model._meta.app_label == 'notes'

        elif model._meta.app_label == 'notes':
            return False

        return None