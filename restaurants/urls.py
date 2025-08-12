from django.urls import path
from .views import RestaurantCreateView, MenuCreateView, TodayMenuListView

urlpatterns = [
    path("", RestaurantCreateView.as_view(), name="create-restaurant"),
    path("<int:pk>/menu/", MenuCreateView.as_view(), name="add-menu"),
    path("menu/today/", TodayMenuListView.as_view(), name="today-menu"),
]
