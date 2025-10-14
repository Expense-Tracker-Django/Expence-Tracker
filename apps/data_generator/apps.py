from django.apps import AppConfig


class DataGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # type: ignore
    name = 'apps.data_generator'
