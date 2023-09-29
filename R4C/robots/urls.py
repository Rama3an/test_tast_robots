from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from robots.views import *

urlpatterns = [
    path('api/updaterobots', csrf_exempt(PutNewRobots.as_view())),
    path('producedrobot/week', csrf_exempt(SaveDateRobots.as_view()))
]
