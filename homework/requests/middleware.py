from models import RequestEntry


class RequestLogMeddleware():

    def process_request(self, request):

        # Log only wanted headers
        headers = (
                   'HTTP_ACCEPT_ENCODING',
                   'HTTP_ACCEPT_LANGUAGE',
                   'HTTP_HOST',
                   'HTTP_REFERER',
                   'HTTP_USER_AGENT',
                   'REMOTE_ADDR',
                   'HTTP_X_REQUESTED_WITH',
                   )

        filtered_headers = {}
        for h in headers:
            if h in request.META:
                filtered_headers[h] = request.META[h]

        req = RequestEntry(
                           path=request.path,
                           method=request.method,
                           params=request.REQUEST,
                           headers=filtered_headers,
                           )
        req.save()

        return None
