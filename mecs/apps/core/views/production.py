from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from mecs.apps.core.models import Production
from mecs.apps.core.serializers.production import ProductionSerializer
from mecs.apps.accounts.permissions import (
    IsAdmin,
    IsOperator,
    IsLeaderOrSupervisor,
)

class ProductionViewSet(ModelViewSet):
    """
    Production API
    - Create: Operator / Leader / Supervisor
    - Update: Leader / Supervisor
    - Delete: Admin only
    """

    serializer_class = ProductionSerializer
    permission_classes = [IsAuthenticated]

    queryset = Production.objects.select_related(
        'machine',
        'leader',
        'prod_parameter',
        'schedule',
    )

    def get_queryset(self):
        qs = super().get_queryset()

        # optional filters
        machine_id = self.request.query_params.get('machine')
        schedule_id = self.request.query_params.get('schedule')
        date = self.request.query_params.get('date')

        if machine_id:
            qs = qs.filter(machine_id=machine_id)

        if schedule_id:
            qs = qs.filter(schedule_id=schedule_id)

        if date:
            qs = qs.filter(created_at__date=date)

        return qs.order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsOperator() | IsLeaderOrSupervisor()]
        if self.action in ['update', 'partial_update']:
            return [IsLeaderOrSupervisor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Centralized create hook.
        Kalau nanti mau:
        - auto assign leader
        - validate vs schedule
        - init counters
        tinggal pindah ke service layer
        """
        serializer.save()
