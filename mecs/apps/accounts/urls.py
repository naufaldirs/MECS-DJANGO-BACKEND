from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, OperatorViewSet, UserViewSet, DepartmentViewSet, GroupViewSet


router = DefaultRouter()

router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'operators', OperatorViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = router.urls 

