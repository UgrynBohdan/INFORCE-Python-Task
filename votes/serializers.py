from rest_framework import serializers
from .models import Vote
from restaurants.models import Menu
from django.utils.timezone import now


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "menu", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        menu = attrs["menu"]

        # Перевірка: чи вже голосував сьогодні
        today = now().date()
        if Vote.objects.filter(employee=user, menu__date=today).exists():
            raise serializers.ValidationError("You have already voted today.")

        # Перевірка: чи меню сьогоднішнє
        if menu.date != today:
            raise serializers.ValidationError("You can only vote for today's menu.")

        return attrs

    def create(self, validated_data):
        validated_data["employee"] = self.context["request"].user
        return super().create(validated_data)


class VoteResultSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField()
    votes_count = serializers.IntegerField()
