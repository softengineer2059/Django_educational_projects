from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


SECRET_KEY = 'django-insecure-sk-h)9^ux%-5)p6y)!me3^p2)*0ob6h1npcxwf6e*lfnwse+4+'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'magazine.apps.MagazineConfig',
    'account.apps.AccountConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'comments.apps.CommentsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'magazine.middleware.ProductViewMiddleware',
]

ROOT_URLCONF = 'minishop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'magazine.context_processors.cart_and_categories',
                'django.template.context_processors.media',
                'magazine.context_processors.recommendations'
            ],
        },
    },
]

WSGI_APPLICATION = 'minishop.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        #'NAME': BASE_DIR / 'goods.db',
        'NAME': 'myshop',
        'USER': 'postgres',
        'PASSWORD': 'qwerty',
        'HOST': 'localhost',
        'PORT': 5432
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [STATIC_DIR]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'