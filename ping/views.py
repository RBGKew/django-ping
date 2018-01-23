import json

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from ping.defaults import *
from ping.checks import checks

@csrf_exempt
def status(request):
    """
    Returns a simple HttpResponse
    """

    response = "<h1>%s</h1>" % getattr(settings, 'PING_DEFAULT_RESPONSE', PING_DEFAULT_RESPONSE)
    content_type = getattr(settings, 'PING_DEFAULT_MIMETYPE', PING_DEFAULT_MIMETYPE)
    response_status = 200

    if request.GET.get('checks') == 'true':
        response_dict = checks(request)
        response += "<dl>"
        for key, value in sorted(response_dict.items()):
            response += "<dt>%s</dt>" % str(key)
            response += "<dd>%s</dd>" % str(value)
            if value != True:
                response_status = 503 # service unavailable if one of the health checks fails
        response += "</dl>"

    if request.GET.get('fmt') == 'json':
        try:
            response = json.dumps(response_dict)
        except UnboundLocalError:
            response_dict = checks(request)
            response = json.dumps(response_dict)
        response = json.dumps(response_dict, sort_keys=True)
        content_type = 'application/json'

    return HttpResponse(response, content_type=content_type, status=response_status)
