"""from django.test import TestCase

from whats_fresh.models import *


class ImageTestCase(TestCase):
    def setUp():
        self.errortext ="" "{
   "error" :{
      "error_status": true,
      "error_name": "not_found_error",
      "error_text": "product with id=232 could not be found",
      "error_level": 10
   },
   "image": "url to image",
   "caption": "text"
}
"" "


possible errors:
    not found (404)
    bad syntax (400)
    missing fields (422)"""
