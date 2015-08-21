from django.core.serializers import json
from whats_fresh.whats_fresh_api.models import Vendor


def is_list(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))


class FreshSerializer(json.Serializer):

    def serialize(self, objects, **kwargs):
        if not is_list(objects):
            objects = [objects]
            return super(FreshSerializer, self).serialize(
                objects, use_natural_foreign_keys=True)[1:-1]
        else:
            return super(FreshSerializer, self).serialize(
                objects, use_natural_foreign_keys=True)

    def get_dump_object(self, obj):
        self._current['id'] = obj.id

        if isinstance(obj, Vendor):
            self._current['lat'] = obj.location.y
            self._current['lng'] = obj.location.x
            del self._current['location']

            self._current['products'] = [
                {
                    'name': pp.product.name,
                    'preparation': pp.preparation.name,
                    'product_id': pp.product.id,
                    'preparation_id': pp.preparation_id
                }
                for pp in obj.products_preparations.all()
            ]

        self._current['ext'] = {}
        return self._current
