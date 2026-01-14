from rest_framework.routers import DefaultRouter
from mecs.apps.core.views.schedule import ScheduleViewSet
from mecs.apps.core.views.daily_production import DailyProductionViewSet
from mecs.apps.core.views.prod_problem import ProdProblemViewSet
from mecs.apps.core.views.production import ProductionViewSet
from mecs.apps.core.views.prod_operation import ProdOperationViewSet
from mecs.apps.core.views.prod_reject import ProdRejectViewSet


router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'daily-productions', DailyProductionViewSet)
router.register(r'prod-problems', ProdProblemViewSet)
router.register(r'productions', ProductionViewSet)
router.register(r'prod-operations', ProdOperationViewSet)
router.register(r'prod-rejects', ProdRejectViewSet)


urlpatterns = router.urls
