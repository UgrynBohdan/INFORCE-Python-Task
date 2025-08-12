from django.db import models
from django.conf import settings
from restaurants.models import Menu

# Create your models here.


class Vote(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "menu")  # щоб за одне меню не можна було проголосувати двічі

    def __str__(self):
        return f"{self.employee} voted for {self.menu}"
