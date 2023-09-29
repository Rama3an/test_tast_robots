from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot
from .models import Order
from .services import send_email


@receiver(post_save, sender=Robot)
def post_save_robot(**kwargs):
    instance = kwargs["instance"]
    order = Order.objects.filter(robot_model=instance.model, robot_version=instance.version)[0]
    if order:
        send_email(order.customer.email, instance.model, instance.version)
