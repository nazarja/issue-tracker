""" Production settings - unsuitable for  development """
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed Hosts
ALLOWED_HOSTS = [os.getenv('HEROKU_HOST_URL')]

# Cors Settings
CORS_URLS_REGEX = r'^/api.*'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [os.getenv('HEROKU_CORS_WHITELIST')]

# email setup - MailGun.com
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_POST = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
EMAIL_MAIN = os.getenv('EMAIL_MAIN')

# stripe keys
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET')

# postgres
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}
