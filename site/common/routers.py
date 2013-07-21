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
        if obj1._meta.app_label == 'notes' or obj2._meta.app_label == 'notes':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == notes_db_name:
            return model._meta.app_label == 'notes'

        elif model._meta.app_label == 'notes':
            return False

        return None

fluid_db_name = 'fluid'

class FluidRouter(object):
    """Controls access to fluid.sqlite"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'fluid':
            return fluid_db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'fluid':
            return fluid_db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'fluid' or obj2._meta.app_label == 'fluid':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == fluid_db_name:
            return model._meta.app_label == 'fluid'

        elif model._meta.app_label == 'fluid':
            return False

        return None