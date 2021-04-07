import dynaconf  # noqa

settings = dynaconf.DjangoDynaconf(
    __name__,
    ENVVAR_PREFIX_FOR_DYNACONF="SCHOOLADMIN",
    ENV_SWITCHER_FOR_DYNACONF="SCHOOLADMIN_ENV",
    SETTINGS_FILE_FOR_DYNACONF="/home/czar/Dev/schooladmin/settings.yaml",
    SECRETS_FOR_DYNACONF="/home/czar/Dev/schooladmin/.secrets.yaml",
    ENVVAR_FOR_DYNACONF="SCHOOLADMIN_SETTINGS",
    INCLUDES_FOR_DYNACONF=["/home/czar/Dev/schooladmin/plugins/*"],
)  # noqa

# don't forget to change the base directory path:
# /home/czar/Dev/schooladmin
# to your own project directory path

# Read more at https://dynaconf.readthedocs.io/en/latest/guides/django.html
