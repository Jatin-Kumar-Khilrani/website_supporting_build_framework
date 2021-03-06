from website import settings

class DatabaseAppsRouter(object):
# 
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'components':
#             return 'cbl'
#         return None
#  
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'components':
#             return 'cbl'
#         return None
#  
#     def allow_relation(self, obj1, obj2, **hints):
#         if obj1._meta.app_label == 'components' or \
#             obj2._meta.app_label == 'components':
#             return True
#         return None
#  
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label == 'components':
#             return db == 'cbl'
#         return None
    
    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None
  
    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None
  
    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None
  
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure that apps only appear in the related database."""
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(app_label) == db
        elif settings.DATABASE_APPS_MAPPING.has_key(app_label):
            return False
        return None