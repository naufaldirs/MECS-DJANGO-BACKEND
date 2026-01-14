from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from mecs.apps.core.models.prod_operation import ProdOperation
from mecs.apps.core.serializers.prod_operation import ProdOperationSerializer
from mecs.apps.accounts.permissions import (
    IsOperator,
    IsLeaderOrSupervisor,
    IsAdmin,
)   
class ProdOperationViewSet(ModelViewSet):
    """
    ProdOperation API
    - Create: Operator
    - Update: Leader / Supervisor
    - Delete: Admin
    - Read: Authenticated
    """

    serializer_class = ProdOperationSerializer
    permission_classes = [IsAuthenticated]

    queryset = ProdOperation.objects.select_related(
        'production',
        'production__machine',
        'production__schedule',
    )

    def get_queryset(self):
        qs = super().get_queryset()

        production_id = self.request.query_params.get('production')
        date = self.request.query_params.get('date')

        if production_id:
            qs = qs.filter(production_id=production_id)

        if date:
            qs = qs.filter(start_time__date=date)

        return qs.order_by('-start_time')

    def get_permissions(self):
        if self.action == 'create':
            return [IsOperator()]
        if self.action in ['update', 'partial_update']:
            return [IsLeaderOrSupervisor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    """
    ProdOperation API
    - Create: Operator
    - Update: Leader / Supervisor
    - Delete: Admin
    - Read: Authenticated
    """

    serializer_class = ProdOperationSerializer
    permission_classes = [IsAuthenticated]

    queryset = ProdOperation.objects.select_related(
        'production',
        'machine',
        'operator',
    )

    def get_queryset(self):
        qs = super().get_queryset()

        production_id = self.request.query_params.get('production')
        machine_id = self.request.query_params.get('machine')

        if production_id:
            qs = qs.filter(production_id=production_id)

        if machine_id:
            qs = qs.filter(machine_id=machine_id)

        return qs.order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsOperator()]
        if self.action in ['update', 'partial_update']:
            return [IsLeaderOrSupervisor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]
