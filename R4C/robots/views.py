from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import ValidationError
from .models import Robot
import json
import pandas as pd


class PutNewRobots(View):
    require_http_methods = ['POST']

    def post(self, request, *args, **kwargs):
        robots_data = json.loads(request.body)
        try:
            new_entry_bd, _ = Robot.objects.get_or_create(
                serial=robots_data.get("serial", "Not set"),
                model=robots_data.get("model", "Not set"),
                version=robots_data.get("version", "Not set"),
                created=robots_data.get("created", timezone.now()),
            )
            new_entry_bd.save()
            return HttpResponse("Записи добавлены")

        except ValidationError:
            return HttpResponse("Ошибка в запросе, проверьте корректность типов")


class SaveDateRobots(View):
    require_http_methods = ['GET']

    def get(self, request, *args, **kwargs):
        day_week_ago = timezone.now() - timezone.timedelta(days=7)
        robots_week = sorted(Robot.objects.filter(created__gte=day_week_ago), key=lambda items: items.model)
        count_robots = {(robot.model, robot.version): 0 for robot in robots_week}
        for robot in robots_week:
            count_robots[(robot.model, robot.version)] += 1

        file_name = f'{request.GET.get("name", "productions_data")}.xlsx'
        sheet_name = None
        with pd.ExcelWriter(file_name) as writer:
            for robot in count_robots.items():
                if robot[0][0] == sheet_name:
                    continue
                sheet_name = robot[0][0]
                table_sheet = pd.DataFrame({"Модель":
                                                [element[0] for element in count_robots if element[0] == sheet_name],
                                            "Версия":
                                                [element[1] for element in count_robots if element[0] == sheet_name],
                                            "Количество":
                                                [element[1] for element in count_robots.items()
                                                 if element[0][0] == sheet_name]
                                            })
                table_sheet.to_excel(writer, sheet_name=sheet_name)
        return HttpResponse("Файл сохранен")
