from djando.urls import path 
from chats.views import home 

urlpattersn=[
  path('',home,name='home'),
]