from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from mecs.apps.core.models import DailyProduction
from mecs.apps.core.serializers.daily_production import (
    DailyProductionSerializer,
)
from mecs.apps.core.services.daily_production import create_daily_production
from mecs.apps.core.serializers.daily_production import DailyProductionSerializer
from mecs.apps.master.models import Machine
from rest_framework.views import APIView
class DailyProductionViewSet(ModelViewSet):
    queryset = DailyProduction.objects.all()
    serializer_class = DailyProductionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        daily = create_daily_production(
            production_date=serializer.validated_data['production_date'],
            status=serializer.validated_data.get('status', 'open'),
        )

        return Response(
            {'id': daily.id, 'production_date': daily.production_date},
            status=status.HTTP_201_CREATED
        )

class DailyProductionDetailView(APIView):
    def get(self, request, report_date):
        daily_production = get_object_or_404(
            DailyProduction.objects.prefetch_related(
                'schedules__productions__machine',
                'schedules__productions__prod_parameter__part',
            ),
            production_date=report_date
        )

        machine = Machine.objects.all()

        return Response({
            'report_id': DailyProductionSerializer(daily_production).data,
            'machines': [
                {'id': m.id, 'name': m.name} for m in machine
            ]
        })