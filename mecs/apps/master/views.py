from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from mecs.apps.master.services.production_capacity import calculate_capacity
from .models import (
    Customer, Machine, Part, ProductionParameter, Shift, ProductionCapacity, ProblemCategory, RejectCategory 
)

from .serializers import (
    CustomerSerializer, MachineSerializer, PartSerializer, ProductionParameterSerializer, ShiftSerializer, ProductionCapacitySerializer, ProblemCategorySerializer, RejectCategorySerializer
)




class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MachineViewSet(ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class PartViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    parser_classes = [MultiPartParser, FormParser]

class ProductionParameterViewSet(ModelViewSet):
    queryset = ProductionParameter.objects.all()
    serializer_class = ProductionParameterSerializer


    @action(detail=True, methods=["get"])
    def capacity(self, request, pk=None):
        parameter = self.get_object()

        try:
            capacity = ProductionCapacity.objects.get(
                prod_parameter=parameter
            )
        except ProductionCapacity.DoesNotExist:
            return Response(
                {"detail": "Capacity not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductionCapacitySerializer(capacity)
        return Response(serializer.data)
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cycle_time = data["cycle_time"]
        cavity = data["cavity"]
        ascast = data["ascast"]
        shot_weight = data["shot_weight"]

        # ✅ VALIDASI DULU
        if cycle_time <= 0:
            raise serializers.ValidationError({"cycle_time": "Harus lebih dari 0"})
        if cavity <= 0:
            raise serializers.ValidationError({"cavity": "Harus lebih dari 0"})
        if ascast > shot_weight:
            raise serializers.ValidationError({"ascast": "Tidak boleh lebih besar dari shot_weight"})

        runner = shot_weight - ascast

        # 1️⃣ Simpan parameter
        parameter = ProductionParameter.objects.create(
            **data,
            runner=runner,
        )

        # 2️⃣ Hitung kapasitas
        capacity_data = calculate_capacity(
            cycle_time=cycle_time,
            cavity=cavity,
            ascast=ascast,
        )

        # 3️⃣ Simpan kapasitas
        ProductionCapacity.objects.create(
            prod_parameter=parameter,
            **capacity_data
        )

        return Response(
            self.get_serializer(parameter).data,
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        parameter = self.get_object()
        serializer = self.get_serializer(parameter, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        ascast = data.get("ascast", parameter.ascast)
        cavity = data.get("cavity", parameter.cavity)
        cycle_time = data.get("cycle_time", parameter.cycle_time)
        shot_weight = data.get("shot_weight", parameter.shot_weight)

        # ✅ VALIDASI
        if cycle_time <= 0:
            raise serializers.ValidationError({"cycle_time": "Harus lebih dari 0"})
        if cavity <= 0:
            raise serializers.ValidationError({"cavity": "Harus lebih dari 0"})
        if ascast > shot_weight:
            raise serializers.ValidationError({"ascast": "Tidak boleh lebih besar dari shot_weight"})

        runner = shot_weight - ascast

        # 1️⃣ Update parameter
        for field, value in data.items():
            setattr(parameter, field, value)

        parameter.runner = runner
        parameter.save()

        # 2️⃣ Hitung ulang kapasitas
        capacity_data = calculate_capacity(
            cycle_time=cycle_time,
            cavity=cavity,
            ascast=ascast,
            shot_weight=shot_weight,
        )

        ProductionCapacity.objects.update_or_create(
            prod_parameter=parameter,
            defaults=capacity_data
        )

        return Response(
            self.get_serializer(parameter).data,
            status=status.HTTP_200_OK
        )


class ProductionCapacityViewSet(ModelViewSet):
    queryset = ProductionCapacity.objects.all()
    serializer_class = ProductionCapacitySerializer

class ProblemCategoryViewSet(ModelViewSet):
    queryset = ProblemCategory.objects.all()
    serializer_class = ProblemCategorySerializer

class RejectCategoryViewSet(ModelViewSet):
    queryset = RejectCategory.objects.all()
    serializer_class = RejectCategorySerializer

class ShiftViewSet(ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer