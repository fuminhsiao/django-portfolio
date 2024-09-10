from rest_framework import viewsets
from .models import Project, Showcase, ProjectBrief, DesignProcess, Page
from .serializers import ProjectSerializer, ShowcaseSerializer, ProjectBriefSerializer, DesignProcessSerializer, PageSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ShowcaseViewSet(viewsets.ModelViewSet):
    queryset = Showcase.objects.all()
    serializer_class = ShowcaseSerializer

class ProjectBriefViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectBrief.objects.all()
    serializer_class = ProjectBriefSerializer

class DesignProcessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignProcess.objects.all()
    serializer_class = DesignProcessSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer