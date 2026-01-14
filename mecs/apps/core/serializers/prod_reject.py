from rest_framework import serializers
from mecs.apps.core.models.prod_reject import ProdReject
from mecs.apps.core.models.prod_operation import ProdOperation
from mecs.apps.master.models import RejectCategory


class ProdRejectSerializer(serializers.ModelSerializer):
    prod_operation_id = serializers.PrimaryKeyRelatedField(
        queryset=ProdOperation.objects.all(),
        source='prod_operation',
        write_only=True
    )

    reject_category_id = serializers.PrimaryKeyRelatedField(
        queryset=RejectCategory.objects.all(),
        source='reject_category',
        write_only=True
    )

    prod_operation = serializers.StringRelatedField(read_only=True)
    reject_category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProdReject
        fields = [
            'id',
            'quantity',
            'reject_photo',
            'reject_category',
            'reject_category_id',
            'prod_operation',
            'prod_operation_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Reject quantity must be greater than zero'
            )
        return value
