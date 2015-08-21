from django.conf import settings

from django.contrib.auth.decorators import user_passes_test
from django.contrib.gis.geos import fromstr


def group_required(*group_names):
    """
    This decorator can be used to protect a view from users not in a given list
    of groups. Add @group_required to a view to require the user to be logged
    in and part of the passed groups. If the user is not a member of the given
    groups, they will be redirected to /login.
    """
    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser | bool(u.groups.filter(name__in=group_names)):
                return True
        return False
    return user_passes_test(in_groups, login_url='/login')


def get_lat_long_prox(request, error=None):
    """
    Parse the latitude, longitude, proximity, and limit for the Vendor
    list functions.

    If the parsing results in an error, the error block is updated to reflect
    that error.
    """
    limit, error = get_limit(request, error)

    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    proximity = request.GET.get('proximity', None)

    point = None

    if lat or lng:
        if proximity:
            try:
                proximity = int(proximity)
            except Exception as e:
                error = {
                    "level": "Warning",
                    "status": True,
                    "name": "Bad proximity",
                    "text": "There was an error finding vendors "
                            "within {0} miles".format(proximity),
                    'debug': "{0}: {1}".format(type(e).__name__, str(e))
                }
                proximity = settings.DEFAULT_PROXIMITY
        else:
            proximity = settings.DEFAULT_PROXIMITY

        try:
            point = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)
        except Exception as e:
            error = {
                "level": "Warning",
                "status": True,
                "name": "Bad location",
                "text": "There was an error with the given "
                        "coordinates {0}, {1}".format(lat, lng),
                'debug': "{0}: {1}".format(type(e).__name__, str(e))
            }

    return [point, proximity, limit, error]


def get_limit(request, error=None):
    """
    Return the limit requested by the user.

    If the limit results in an error, the error block is updated to reflect
    that error.
    """
    limit = request.GET.get('limit', None)
    if limit is None:
        return [limit, error]
    try:
        return [int(limit), error]
    except Exception as e:
        error = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Warning',
            'text': 'Invalid limit. Returning all results.',
            'name': 'Bad Limit'
        }
        return [None, error]
