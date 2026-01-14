from rest_framework import serializers
from mecs.apps.core.models.prod_problem import ProdProblem
from mecs.apps.core.models.prod_operation import ProdOperation
from mecs.apps.master.models import ProblemCategory


class ProdProblemSerializer(serializers.ModelSerializer):
    prod_operation_id = serializers.PrimaryKeyRelatedField(
        queryset=ProdOperation.objects.all(),
        source='prod_operation',
        write_only=True
    )

    problem_category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProblemCategory.objects.all(),
        source='problem_category',
        write_only=True
    )

    prod_operation = serializers.StringRelatedField(read_only=True)
    problem_category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProdProblem
        fields = [
            'id',
            'duration',
            'action',
            'problem_category',
            'problem_category_id',
            'prod_operation',
            'prod_operation_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_duration(self, value):
        if value.total_seconds() <= 0:
            raise serializers.ValidationError(
                'Duration must be greater than zero'
            )
        return value
