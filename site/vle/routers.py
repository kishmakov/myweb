fluids_db_name = 'fluids'

class VleRouter(object):
    """Controls access to vle databases."""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'vle':
            return fluids_db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'vle':
            return fluids_db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'vle' or obj2._meta.app_label == 'vle':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the vle app only appears on the 'simple_fluids' db"

        if db == fluids_db_name:
            return model._meta.app_label == 'vle'

        elif model._meta.app_label == 'vle':
            return False

        return None
