DEBUG = False
BASEDIR = ''
SUBDIR = ''
PREFIX = ''
QUALITY = 85
CONVERT = '/usr/bin/convert'
WVPS = '/usr/bin/wvPS'
EXTENSION = 'jpg'
PROCESSORS = (
    'extra.thumbnail.processors.colorspace',
    'extra.thumbnail.processors.autocrop',
    'extra.thumbnail.processors.scale_and_crop',
    'extra.thumbnail.processors.filters',
)
IMAGEMAGICK_FILE_TYPES = ('eps', 'pdf', 'psd')
