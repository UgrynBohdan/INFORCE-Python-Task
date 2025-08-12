from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now

from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer

# Create your views here.


# POST /api/restaurants/
class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# POST /api/restaurants/{id}/menu/
class MenuCreateView(APIView):
    def post(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /api/restaurants/menu/today/
class TodayMenuListView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        today = now().date()
        return Menu.objects.filter(date=today)
