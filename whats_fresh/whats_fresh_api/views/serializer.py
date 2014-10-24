from django.core.serializers import json
from whats_fresh.whats_fresh_api.models import Vendor, Story


class FreshSerializer(json.Serializer):

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
