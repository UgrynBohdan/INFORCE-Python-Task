from django.urls import path
from .views import RestaurantCreateView, MenuCreateView, TodayMenuListRouter

urlpatterns = [
    path("", RestaurantCreateView.as_view(), name="create-restaurant"),
    path("<int:pk>/menu/", MenuCreateView.as_view(), name="add-menu"),
    path("menu/today/", TodayMenuListRouter.as_view(), name="today-menu"),
]
