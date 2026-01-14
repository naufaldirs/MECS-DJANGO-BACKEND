from rest_framework import serializers
from .models import Employee, Operator, Department, User
from django.contrib.auth.models import Group




class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']



class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",
        write_only=True
    )

    def get_photo(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None

    class Meta:
        model = Employee
        fields = [
            "id",
            "nip",
            "full_name",
            "phone_number",
            "gender",
            "photo",
            "department",
            "department_id",
        ]



class UserSerializer(serializers.ModelSerializer):
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    groups = serializers.StringRelatedField(many=True, read_only=True)

    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
    queryset=Employee.objects.all(), source='employee', write_only=True
    )


    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "employee",
            "employee_id",
            "groups",
            "group_ids",
        ]

    def create(self, validated_data):
        groups = validated_data.pop("group_ids", [])
        user = super().create(validated_data)
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop("group_ids", None)
        user = super().update(instance, validated_data)
        if groups is not None:
            user.groups.set(groups)
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

class OperatorSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
    queryset=Employee.objects.all(), source='employee', write_only=True
)
    class Meta:
        model = Operator
        fields = ['id', 'employee', 'employee_id', 'group']