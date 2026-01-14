from rest_framework import serializers
from mecs.apps.core.models.prod_operation import ProdOperation
from mecs.apps.core.models.production import Production


class ProdOperationSerializer(serializers.ModelSerializer):
    production_id = serializers.PrimaryKeyRelatedField(
        queryset=Production.objects.all(),
        source='production',
        write_only=True
    )

    production = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProdOperation
        fields = [
            'id',
            'start_time',
            'end_time',
            'plan',
            'actual',
            'production',
            'production_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        start = attrs.get('start_time')
        end = attrs.get('end_time')

        if start and end and start >= end:
            raise serializers.ValidationError(
                'end_time must be greater than start_time'
            )

        return attrs
