import logging
from datetime import datetime
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