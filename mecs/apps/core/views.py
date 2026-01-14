from rest_framework.viewsets import ModelViewSet
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.permissions import IsAuthenticated

from mecs.apps.accounts.permissions import (
    IsAdmin,
    IsPPC,
    IsOperator,
    IsLeaderOrSupervisor,
)

class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.select_related(
        'shift', 'machine', 'part'
    )
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        date = self.request.query_params.get('date')
        if date:
            qs = qs.filter(production_date=date)

        return qs
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsPPC()]
        if self.action in ['update', 'partial_update']:
            return [IsOperator() | IsLeaderOrSupervisor()]
        if self.action in ['destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]