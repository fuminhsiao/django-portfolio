from rest_framework import serializers
from .models import Project, Showcase, ProjectBrief, Tag, DesignProcess, ProcessStep, DesignProcessStep, Page, TextLayer, ImageLayer, VideoLayer, ImageLayerLink

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ShowcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showcase
        fields = '__all__'

class ProjectBriefSerializer(serializers.ModelSerializer):
    project_des = serializers.CharField(source='project.description')
    project_title = serializers.CharField(source='project.title')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectBrief
        fields = ['project_des', 'project_title', 'tags']

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = ['name']

class DesignProcessStepSerializer(serializers.ModelSerializer):
    process_step = ProcessStepSerializer()

    class Meta:
        model = DesignProcessStep
        fields = ['process_step', 'order']

class DesignProcessSerializer(serializers.ModelSerializer):
    steps = DesignProcessStepSerializer(source='designprocessstep_set', many=True, read_only=True)

    class Meta:
        model = DesignProcess
        fields = ['project', 'steps']

class TextLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextLayer
        fields = ['title', 'text', 'order']

class ImageLayerLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLayerLink
        fields = ['title', 'url', 'description']  # Fields for the link

class ImageLayerSerializer(serializers.ModelSerializer):
    links = ImageLayerLinkSerializer(many=True, read_only=True)  # Include links

    class Meta:
        model = ImageLayer
        fields = ['image', 'alt_text', 'order', 'title', 'text', 'links']  # Updated fields

class VideoLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLayer
        fields = ['video_url', 'order']

class PageSerializer(serializers.ModelSerializer):
    text_layers = TextLayerSerializer(many=True, read_only=True)
    image_layers = ImageLayerSerializer(many=True, read_only=True)  # Updated to use the new ImageLayerSerializer
    video_layers = VideoLayerSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['title', 'text_layers', 'image_layers', 'video_layers']

class ProjectSerializer(serializers.ModelSerializer):
    briefs = ProjectBriefSerializer(many=True, read_only=True)
    showcases = ShowcaseSerializer(many=True, read_only=True)
    design_processes = DesignProcessSerializer(many=True, read_only=True)
    pages = PageSerializer(many=True, read_only=True)  # Includes updated PageSerializer

    class Meta:
        model = Project
        fields = '__all__'
