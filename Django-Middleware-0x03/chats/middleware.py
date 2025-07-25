import logging
from datetime import datetime,time
from django.utils import timezone
import time
from django.http imprt JsonResponse
from django.http import HttpResponseForbidden

#  to create the log 
logger = logging.getLogger(__name__)
handler =logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
class RequestLoggingMiddleware:
  def __init__(self,get_response):
    self.get_response = get_response
  def __call__(self,request):
    user = request.user if request.user.is_authenticated else 'Anonymous'
    logger.info(f"User:{user} - Path:{request.path}")
    response= self.get_response(request)
    return response

# restrict access after a specific time 
class RestrictAccessByTimeMiddleware:
  def __init__(self,get_response):
    self.get_response=get_response
  def __call__(self,request):
    current_time = datetime.now().time()
    limit_time1 = time(18,0)
    limit_time2 = time(21,0)
    if not (start_time <= current_time <= end_time):
      return HttpResponseForbidden("Access is only allowed between 6 PM and 9 PM.")



    response = self.get_response(request)
    return response


# offensive language middleware
class OffensiveLanguageMiddleware:
  def __init__(self,get_response):
    self.get_response=get_response
    self.rate_limit = 5
    self.time_window = 60
    self.message_log ={}
  def __call__(self,request):
    ip=self.get_client_ip(request)
    current_time=time.time()
    if request.path.startswith('/api/messages') and requests.method =='POST':
      timestamps= self.message_log.get(ip,[])
      timestamps = [t for t in timestamps if current_time - t < self.time_window]

            if len(timestamps) >= self.rate_limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Max 5 messages per minute allowed."},
                    status=429
                )

            timestamps.append(current_time)
            self.message_log[ip] = timestamps 

    return self.get_response(request)

    def get_client_ip(self, request):
        # Check for IP in X-Forwarded-For if behind a proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip