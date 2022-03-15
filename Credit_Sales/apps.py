from django.apps import AppConfig


class CreditSalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Credit_Sales'

    def ready(self):
        from Credit_Sales import signals