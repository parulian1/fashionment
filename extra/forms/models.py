from django.db.models import IntegerField

class BigIntegerField(IntegerField):
  def db_type(self):
    return 'bigint'
