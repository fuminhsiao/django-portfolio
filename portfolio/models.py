from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Showcase(models.Model):
    project = models.ForeignKey(Project, related_name='showcases', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='showcase_images/')
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Showcase for {self.project.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProjectBrief(models.Model):
    project = models.ForeignKey(Project, related_name='briefs', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Brief for {self.project.title}"
    
class ProcessStep(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DesignProcess(models.Model):
    project = models.ForeignKey(Project, related_name='design_processes', on_delete=models.CASCADE)
    steps = models.ManyToManyField(ProcessStep, through='DesignProcessStep')

    def __str__(self):
        return f"Process for {self.project.title}"

class DesignProcessStep(models.Model):
    design_process = models.ForeignKey(DesignProcess, on_delete=models.CASCADE)
    process_step = models.ForeignKey(ProcessStep, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.process_step.name} in {self.design_process.project.title}"

class Page(models.Model):
    project = models.ForeignKey(Project, related_name='pages', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Layer(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.IntegerField(editable=True)  # 设置为不可编辑

    class Meta:
        abstract = True
        ordering = ['order']

class TextLayer(Layer):
    page = models.ForeignKey(Page, related_name='text_layers', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk is None:  # 仅在新建对象时自动设置 order
            last_order = TextLayer.objects.filter(page=self.page).count()
            self.order = last_order
        super().save(*args, **kwargs)

class ImageLayer(Layer):  # 继承自 Layer 类
    page = models.ForeignKey(Page, related_name='image_layers', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_layers/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:  # 仅在新建对象时自动设置 order
            last_order = ImageLayer.objects.filter(page=self.page).count()
            self.order = last_order
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f"ImageLayer on {self.page.title}"

class ImageLayerLink(models.Model):
    image_layer = models.ForeignKey(ImageLayer, related_name='links', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)  # New title field
    url = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description for the link

    def __str__(self):
        return f"Link '{self.title}' for {self.image_layer.title or 'ImageLayer'}"

class VideoLayer(Layer):
    page = models.ForeignKey(Page, related_name='video_layers', on_delete=models.CASCADE)
    video_url = models.URLField()

    def save(self, *args, **kwargs):
        if self.pk is None:  # 仅在新建对象时自动设置 order
            last_order = VideoLayer.objects.filter(page=self.page).count()
            self.order = last_order
        super().save(*args, **kwargs)





