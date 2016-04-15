"""
Classes representing uploaded files.
"""

import os

from django.conf import settings
from django.core.files import temp as tempfile
from django.core.files.uploadedfile import TemporaryUploadedFile as TUF
from django.core.exceptions import ImproperlyConfigured

__all__ = ('TemporaryUploadedFile',)

class TemporaryUploadedFile(TUF):
    """
    A file uploaded to a temporary location (i.e. stream-to-disk).
    """
    def __init__(self, *args, **kwargs):
        FILE_UPLOAD_TEMP_DIR = getattr(settings,'FILE_UPLOAD_TEMP_DIR','')
        if FILE_UPLOAD_TEMP_DIR:
            if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
                os.makedirs(FILE_UPLOAD_TEMP_DIR)

            file = tempfile.NamedTemporaryFile(suffix='.upload',
                dir=FILE_UPLOAD_TEMP_DIR)
        else:
            raise ImproperlyConfigured, 'Settings must have "FILE_UPLOAD_TEMP_DIR"'
            #file = tempfile.NamedTemporaryFile(suffix='.upload')
        super(TemporaryUploadedFile, self).__init__(*args,**kwargs)
