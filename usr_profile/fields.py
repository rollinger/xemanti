from django.db import models
from django.core import exceptions

from south.modelsinspector import add_introspection_rules

class MoneyField(models.IntegerField):
    __metaclass__ =  models.SubfieldBase
    
    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        return int(value * 100)

    def to_python(self, value):
        if value is None or isinstance(value, float):
            return value
        try:
            return float(value) / 100
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                "This value must be an integer or a string represents an integer.")

    def formfield(self, **kwargs):
        from django.forms import FloatField
        defaults = {'form_class': FloatField}
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)
add_introspection_rules([], ["^usr_profile\.fields\.MoneyField"])