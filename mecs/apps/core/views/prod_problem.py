from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from mecs.apps.core.models.prod_problem import ProdProblem
from mecs.apps.core.serializers.prod_problem import ProdProblemSerializer
from mecs.apps.accounts.permissions import (
    IsOperator,
    IsLeaderOrSupervisor,
    IsAdmin,
)

class ProdProblemViewSet(ModelViewSet):
    """
    ProdProblem API
    - Create: Operator
    - Update: Leader / Supervisor
    - Delete: Admin
    - Read: Authenticated
    """

    serializer_class = ProdProblemSerializer
    permission_classes = [IsAuthenticated]

    queryset = ProdProblem.objects.select_related(
        'problem_category',
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
            qs = qs.filter(problem_category_id=category_id)

        return qs.order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsOperator()]
        if self.action in ['update', 'partial_update']:
            return [IsLeaderOrSupervisor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]
    def perform_create(self, serializer):
        serializer.save()