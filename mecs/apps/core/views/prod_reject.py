from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from mecs.apps.core.models.prod_reject import ProdReject
from mecs.apps.core.serializers.prod_reject import ProdRejectSerializer
from mecs.apps.accounts.permissions import (
    IsOperator,
    IsLeaderOrSupervisor,
    IsAdmin,
)

class ProdRejectViewSet(ModelViewSet):
    """
    ProdReject API
    - Create: Operator
    - Update: Leader / Supervisor
    - Delete: Admin
    - Read: Authenticated
    """

    serializer_class = ProdRejectSerializer
    permission_classes = [IsAuthenticated]

    queryset = ProdReject.objects.select_related(
        'reject_category',
        'prod_operation',
        'prod_operation__production',
    )

    def get_queryset(self):
        qs = super().get_queryset()

        operation_id = self.request.query_params.get('operation')
        category_id = self.request.query_params.get('category')

        if operation_id:
            qs = qs.filter(prod_operation_id=operation_id)

        if category_id:
            qs = qs.filter(reject_category_id=category_id)

        return qs.order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsOperator()]
        if self.action in ['update', 'partial_update']:
            return [IsLeaderOrSupervisor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]
