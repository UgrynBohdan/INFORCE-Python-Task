from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.timezone import now

from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer


# POST /api/restaurants/  — доступно лише авторизованим
class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]   # або можна не вказувати, якщо DEFAULT_PERMISSION_CLASSES = IsAuthenticated


# POST /api/restaurants/{id}/menu/ — доступно лише авторизованим
class MenuCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            # перевірка unique_together (restaurant, date) може викликати IntegrityError, можна перевірити заздалегідь:
            date = serializer.validated_data.get('date') # type: ignore
            if Menu.objects.filter(restaurant=restaurant, date=date).exists():
                return Response({"detail": "Menu for this restaurant and date already exists"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /api/restaurants/menu/today/ — відкрито для всіх
class TodayMenuListRouter(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if getattr(request, "is_legacy_client", False):
            return TodayMenuListViewV1.as_view()(request._request, *args, **kwargs)
        else:
            return TodayMenuListViewV2.as_view()(request._request, *args, **kwargs)


# --- TODAY MENU V1 (Legacy) ---
class TodayMenuListViewV1(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "This is a legacy version of the API. Please update your app."})


# --- TODAY MENU V2 (Current logic) ---
class TodayMenuListViewV2(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        today = now().date()
        return Menu.objects.filter(date=today)
