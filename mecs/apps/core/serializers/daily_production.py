from rest_framework import serializers
from mecs.apps.core.models.daily_production import DailyProduction


class DailyProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProduction
        fields = [
            'production_date',
            'status',
        ]

