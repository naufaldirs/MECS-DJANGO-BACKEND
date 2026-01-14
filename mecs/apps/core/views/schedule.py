from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from mecs.apps.master.models import Part, Machine
from mecs.apps.master.serializers import PartSerializer
from mecs.apps.core.models.daily_production import DailyProduction
from mecs.apps.core.models import Schedule
from mecs.apps.core.serializers.schedule import (
    ScheduleSerializer,
    ScheduleAssignSerializer,
)
from mecs.apps.core.services.schedule_assignment import (
    assign_production_to_schedule,
)
from mecs.apps.accounts.permissions import IsPPC
from rest_framework.views import APIView

class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.select_related('shift')
    serializer_class = ScheduleSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsPPC],
    )
    def assign(self, request, pk=None):
        serializer = ScheduleAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        production = assign_production_to_schedule(
            schedule_id=pk,
            **serializer.validated_data
        )

        return Response(
            {
                'success': True,
                'production_id': production.id,
            },
            status=status.HTTP_200_OK
        )

class ScheduleDetailContextView(APIView):
    def get(self, request, schedule_id):
        report_id = request.query_params.get('daily_production_id')
        machine_id = request.query_params.get('machine_id')
        shift = request.query_params.get('shift')

        report = get_object_or_404(DailyProduction, id=report_id)
        machine = get_object_or_404(Machine, id=machine_id)

        schedule = get_object_or_404(
            report.schedules,
            id=schedule_id,
            shift=shift
        )

        parts = Part.objects.select_related(
            'customer'
        ).prefetch_related(
            'parameters'
        ).order_by('-customer_id')

        return Response({
            'daily_production_id': report.id,
            'machine': {'id': machine.id, 'name': machine.name},
            'shift': shift,
            'schedule_id': schedule.id,
            'parts': PartSerializer(parts, many=True).data
        })
