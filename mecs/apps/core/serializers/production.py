from rest_framework import serializers
from mecs.apps.accounts.models import User,Operator
from mecs.apps.core.models.production import Production
from mecs.apps.master.serializers import MachineSerializer, ProductionParameterSerializer
from mecs.apps.master.models import Machine, ProductionParameter
from mecs.apps.core.serializers.schedule import ScheduleSerializer
from mecs.apps.core.models.schedule import Schedule

class ProductionSerializer(serializers.ModelSerializer):
    machine = MachineSerializer(read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(), source='machine', write_only=True
    )
    leader = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='leader'),
        allow_null=True,
        required=False
    )
    prod_parameter = ProductionParameterSerializer(read_only=True)
    prod_parameter_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductionParameter.objects.all(), source='prod_parameter', write_only=True
    )
    schedule = ScheduleSerializer(read_only=True)
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(), source='schedule', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Production
        fields = [
            'id', 'total_shoots', 'machine', 'machine_id',
            'leader', 'prod_parameter', 'prod_parameter_id',
            'schedule', 'schedule_id',
            'created_at', 'updated_at'
        ]
