from rest_framework.viewsets import ModelViewSet
from .models import Employee, Operator, User, Department
from .serializers import EmployeeSerializer, OperatorSerializer, UserSerializer, DepartmentSerializer, GroupSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class OperatorViewSet(ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().select_related("employee").prefetch_related("groups")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
