from django.core.serializers import json


class CleanSerializer(json.Serializer):

    def use_natural_keys(self):
        self.use_natural_keys = True

    def get_dump_object(self, obj):
        self._current['id'] = obj.id
        return self._current

    def handle_fk_field(self, obj, field):
        if hasattr(field.rel.to, 'natural_key'):
            related = getattr(obj, field.name)
            if related:
                value = related.natural_key()
            else:
                value = None
        else:
            value = getattr(obj, field.get_attname())
        self._current[field.name] = value