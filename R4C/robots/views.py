from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import ValidationError
from .models import Robot
import json


class PutNewRobots(View):
    def post(self, request, *args, **kwargs):
        robots_data = json.loads(request.body)
        try:
            new_entry_bd, _ = Robot.objects.get_or_create(
                serial=robots_data.get("serial", "Not set"),
                model=robots_data.get("model", "Not set"),
                version=robots_data.get("version", "Not set"),
                created=robots_data.get("created", "Not set"),
            )
            return HttpResponse("Записи добавлены")

        except ValidationError:
            return HttpResponse("Ошибка в запросе, проверьте корректность типов")