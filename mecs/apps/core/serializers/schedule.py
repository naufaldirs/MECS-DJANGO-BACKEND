from rest_framework import serializers
from mecs.apps.core.models.daily_production import DailyProduction
from mecs.apps.core.models.schedule import Schedule
from mecs.apps.master.models import  Machine, ProductionParameter


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'id',
            'scheduled_time',
            'shift',
            'created_at',
            'updated_at',
        ]

class ScheduleAssignSerializer(serializers.Serializer):
    prod_parameter_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductionParameter.objects.all(),
        source='prod_parameter'
    )
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        source='machine'
    )
    daily_production_id = serializers.PrimaryKeyRelatedField(
        queryset=DailyProduction.objects.all(),
        source='daily_production'
    )
    target_time = serializers.ChoiceField(choices=[6, 7, 8])
    target_pcs = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    details = serializers.ListField(child=serializers.DictField())

