from django.db import models
from django.utils.encoding import smart_str, smart_unicode
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json


class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value == "" or value is None:
            return None
        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            try:
                return eval(value)
            except ValueError:
                pass

        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert our JSON object to a string before we save"""
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_db_prep_value(value, connection=connection, prepared=prepared)

# rules for South migrations tool (for version >= 0.7)
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^apps\.page\.fields\.JSONField"])
except ImportError:
    pass

class JsonListField(JSONField):
    def add(value, key=None):
        key = key if key else 'items'
        if key not in self.value:
            self.value[key] = []

        self.value[key].append(value)

        return self.value[key]

    def delete(key):
        if key not in self.value:
            return True
        else:
            del self.value[key]
        return self.value

