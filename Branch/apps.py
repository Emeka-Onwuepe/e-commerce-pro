from django.apps import AppConfig


class BranchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Branch'
    
    def ready(self):
        from Branch import signals
        # return super().ready()
