from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ShowcaseViewSet, ProjectBriefViewSet, DesignProcessViewSet, PageViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'showcases', ShowcaseViewSet)
router.register(r'projectbriefs', ProjectBriefViewSet)
router.register(r'design_processes', DesignProcessViewSet)
router.register(r'pages', PageViewSet)  # 新增 TextLayer 的路由

urlpatterns = [
    path('', include(router.urls)),
]
