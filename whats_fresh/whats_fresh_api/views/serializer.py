from django.core.serializers import json


class FreshSerializer(json.Serializer):
    """
    def __init__(self, *args, **kwargs):
        self.use_natural_foreign_keys = kwargs.get("use_natural_foreign_keys", False)
        super(FreshSerializer, self).__init__(*args, **kwargs)"""

    def get_dump_object(self, obj):
        self._current['id'] = obj.id
        return self._current

"""
    def handle_fk_field(self, obj, field):
        if hasattr(field.rel.to, 'natural_key'):
            related = getattr(obj, field.name)
            if related:
                value = related.natural_key()
            else:
                value = None
        else:
            value = getattr(obj, field.get_attname())
        self._current[field.name] = value"""