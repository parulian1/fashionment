# Django settings for fashion project.
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG
STATIC_MEDIA=True
SSL=False
ADMINS = (
     ('Robin', 'robinchew@gmail.com'),
     ('Martogi', 'craker_devil84@yahoo.com'),
)

BASE_DIR= os.path.dirname(__file__)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = 'fashion.db'             # Or path to database file if using sqlite3.
DATABASE_NAME = 'fashion.sqlite' 
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Jakarta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')+'/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^xq_o=ow3y0b-%bqa11fp7gx^hu=qks2ao$de8=qqo+s$1ioqy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #"django.middleware.cache.CacheMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'extra.middleware.ReCaptchaMiddleware',
    #'extra.cache_smart.SmartCacheNode',
    'fashion.middleware.MobileTemplatesMiddleware',
)

ROOT_URLCONF = 'fashion.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

MOBILE_TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates', 'mobile'),
)

DJAPIAN_DATABASE_PATH = os.path.join(BASE_DIR, 'djapian_data')+'/'
DJAPIAN_STEMMING_LANG = "en"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    #'clothing',
    'compressor',
    'accounts',
    'store',
    'coltrane',
    'tagging',
    'mail',
    'sorl.thumbnail',
    'extra',
    'djapian',
    'pagination',
    'ads',
    'horoscope',
    'magazine',
    'pageflip',
)

LOGIN_REDIRECT_URL='/'
LOGIN_URL='/account/login/'

ACCOUNT_ACTIVATION_DAYS=7
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mailer@fashionment.com'
EMAIL_HOST_PASSWORD = 'emimailer1'
EMAIL_PORT = 587
COMPANY_EMAIL = {
  'info':('Information','customer-support@fashionment.com'),
  'sales':('Sales','customer-support@fashionment.com'),
  'account':('Account','customer-support@fashionment.com'),
  'critic':('Criticism','customer-support@fashionment.com'),
}
TEMPLATE_CONTEXT_PROCESSORS=(
  "django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  "fashion.accounts.context_processors.user",
  "fashion.accounts.context_processors.login_form",
  "fashion.context_processors.previous_url",
  "fashion.context_processors.use_google_search",
  "fashion.context_processors.use_google_analytics",
  "fashion.magazine.context_processors.show_magazine",
#  "fashion.context_processors.query",
)
LOGIN_REDIRECT_URL='/'
LOGIN_URL='/account/login/'
CACHE_BACKEND = 'file://%s' % os.path.join(BASE_DIR,'django_cache')
#CACHE_BACKEND = 'locmem:///'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX='fn'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True
#RECAPTCHA_PUBLIC = '6Lc49AUAAAAAAKCmiwBJumY1rsN70R4ijxMyqjat'
#RECAPTCHA_PRIVATE = '6Lc49AUAAAAAANwTboQssL6EKMf_5HiP7h6kfq1q'
RECAPTCHA_PUBLIC = '6LfKgQYAAAAAAETRzfjR7yGd1-qegj2MzCfftb5G'
RECAPTCHA_PRIVATE = '6LfKgQYAAAAAALEigAvGtr3vsp8MLhwCm3xp7V31'
MAX_UPLOAD_SIZE=2100000
FIXTURE_DIRS=(
  #'fixture/auth/',
  #'fixture/store/',
  #'fixture/accounts/',
  #'fixture/flatpages',
  #'fixture/coltrane',
)
FILE_UPLOAD_HANDLERS=(
    "extra.core.files.uploadhandler.TemporaryFileUploadHandler",
)
FILE_UPLOAD_TEMP_DIR=os.path.join(MEDIA_ROOT,'tmp')+'/'
FILE_UPLOAD_TEMP_URL_DIR=os.path.join(MEDIA_URL,'tmp')+'/'
MAILHIDE_PUB_KEY = '01kY8oCJ5P8-HRUF283RHNeg=='
MAILHIDE_PRIV_KEY = 'B14D6357C5F5D5323F01B88CF7B240D9'
