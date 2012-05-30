ugettext = lambda s: s

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
LANGUAGES = (
    ('en', ugettext('English')),
    ('id', ugettext('Indonesian')),
    ('es', ugettext('Spanish')),
    ('pt', ugettext('Portuguese')),
    ('sv', ugettext('Swedish')),
)
LANGUAGE_COOKIE_NAME = "language"
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = "en"
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ";psbn&"
DECIMAL_SEPARATOR = "."
