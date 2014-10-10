from django.core.serializers import json


class FreshSerializer(json.Serializer):
    def get_dump_object(self, obj):
        self._current['id'] = obj.id
        return self._current