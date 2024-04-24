from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import Taskviewset

router=DefaultRouter()
router.register("v2/task",Taskviewset,basename="tasks")

urlpatterns=[
    
]+router.urls