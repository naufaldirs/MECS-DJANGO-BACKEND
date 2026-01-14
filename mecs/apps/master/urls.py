from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, MachineViewSet, PartViewSet, ProductionParameterViewSet, RejectCategoryViewSet, ProblemCategoryViewSet 
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'parts', PartViewSet)
router.register(r'parameters', ProductionParameterViewSet)
router.register(r'rejects', RejectCategoryViewSet)
router.register(r'problems', ProblemCategoryViewSet)

urlpatterns = router.urls

