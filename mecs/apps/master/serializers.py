from .models import Customer, Machine, Part, ProductionParameter, Shift, ProductionCapacity, ProblemCategory, RejectCategory
from rest_framework import serializers



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id' ,'name', 'address']




class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'line_address', 'status']




class PartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
    queryset=Customer.objects.all(), source='customer', write_only=True, required=False
    )


    class Meta:
        model = Part
        fields = ['id', 'part_number', 'part_name', 'model', 'photo', 'customer', 'customer_id']




class ProductionParameterSerializer(serializers.ModelSerializer):
    part = PartSerializer(read_only=True)
    part_id = serializers.PrimaryKeyRelatedField(
    queryset=Part.objects.all(), source='part', write_only=True
    )
    runner = serializers.IntegerField(read_only=True)


    class Meta:
        model = ProductionParameter
        fields = ['id', 'part', 'part_id', 'type', 'cavity', 'runner', 'shot_weight', 'ascast', 'cycle_time']


class ProductionCapacitySerializer(serializers.ModelSerializer):
    prod_parameter = ProductionParameterSerializer(read_only=True)
    prod_parameter_id = serializers.PrimaryKeyRelatedField(
    queryset=ProductionParameter.objects.all(), source='prod_parameter', write_only=True
    )


    class Meta:
        model = ProductionCapacity
        fields = ['id', 'normal_kg', 'overtime_kg', 'dandory_kg', 'one_hour_pcs', 'six_hour_pcs',
                  'seven_hour_pcs', 'eight_hour_pcs', 'prod_parameter', 'prod_parameter_id']

class ProblemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCategory
        fields = ['id', 'name', 'description', 'solution']

class RejectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectCategory
        fields = ['id', 'name', 'description', 'sample_photo']

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['id', 'name', 'start_time', 'end_time']