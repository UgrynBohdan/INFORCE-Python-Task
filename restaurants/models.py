from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    date = models.DateField()
    items = models.JSONField()  # [{ "dish": "Pizza", "price": 12.5 }, ...]

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("restaurant", "date")  # одне меню на день для ресторану

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"
