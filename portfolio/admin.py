from django.contrib import admin
from .models import Project, ProjectBrief, Showcase, Tag, DesignProcess, ProcessStep, DesignProcessStep, Page, TextLayer, ImageLayer, VideoLayer, ImageLayerLink

# 注册 Tag 模型
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 注册 ProjectBrief 模型
@admin.register(ProjectBrief)
class ProjectBriefAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__title',)
    filter_horizontal = ('tags',)  # 使用水平过滤器来选择多对多字段（tags）

# 注册 Showcase 模型
@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__title',)
    list_filter = ('project',)

# 注册 Project 模型
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)  # 只显示项目的标题
    search_fields = ('title',)
    inlines = []  # 如果需要在 Project 中编辑其相关的 Showcase 或 ProjectBrief，可以在这里添加 inline

# 注册 ProcessStep 模型
@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 注册中介模型 DesignProcessStep
class DesignProcessStepInline(admin.TabularInline):
    model = DesignProcessStep
    extra = 1  # 在 admin 中额外显示一行空白记录，方便添加

# 注册 DesignProcess 模型
@admin.register(DesignProcess)
class DesignProcessAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__title',)
    inlines = [DesignProcessStepInline]  # 通过 inline 形式管理步骤及其顺序

# 添加 ImageLayerLink 的 inline 管理
class ImageLayerLinkInline(admin.TabularInline):
    model = ImageLayerLink
    fields = ['title', 'url', 'description']  # Include title field in the inline
    extra = 1  # Display one extra empty field
    
# 添加 Page 和 Layer 管理
class TextLayerInline(admin.StackedInline):
    model = TextLayer
    extra = 1

class ImageLayerInline(admin.StackedInline):
    model = ImageLayer
    extra = 1
    inlines = [ImageLayerLinkInline]  # 为 ImageLayer 增加内联的 Link 管理

class VideoLayerInline(admin.StackedInline):
    model = VideoLayer
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'project')
    search_fields = ('title', 'project__title')
    inlines = [TextLayerInline, ImageLayerInline, VideoLayerInline]  # 在 Page 中内联不同的 Layer 模型

@admin.register(ImageLayer)
class ImageLayerAdmin(admin.ModelAdmin):
    list_display = ('title', 'page')
    inlines = [ImageLayerLinkInline]  # Attach the inline for managing links