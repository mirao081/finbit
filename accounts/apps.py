
fromdjango.appsimportAppConfig


classAccountsConfig(AppConfig):

    default_auto_field="django.db.models.BigAutoField"

name="accounts"

defready(self):
        importaccounts.signals

