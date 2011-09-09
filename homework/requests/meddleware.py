from models import RequestEntry


class RequestLogMeddleware():
    
    def process_request(self, request):
        req = RequestEntry(
                           path=request.get_full_path(),
                           method=request.method,
                           params=request.REQUEST,
                           headers=request.META,
                           )
        req.save()
        
        return None
