import json
import os
from django.core.management.base import BaseCommand
from portfolio.models import (
    Project, Showcase, Tag, ProjectBrief, ProcessStep, DesignProcess, DesignProcessStep,
    Page, TextLayer, ImageLayer, VideoLayer, ImageLayerLink
)

class Command(BaseCommand):
    help = 'Export data to JSON file'

    def handle(self, *args, **kwargs):
        # 导出项目数据
        projects = Project.objects.all()
        data = []

        for project in projects:
            project_data = {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'showcases': [
                    {
                        'id': showcase.id,
                        'image': showcase.image.url if showcase.image else None,
                        'link': showcase.link
                    } for showcase in project.showcases.all()
                ],
                'tags': [
                    {'id': tag.id, 'name': tag.name} 
                    for brief in project.briefs.all() 
                    for tag in brief.tags.all()
                ],
                'design_processes': [
                    {
                        'id': process.id,
                        'steps': [
                            {
                                'id': step.process_step.id,
                                'name': step.process_step.name,
                                'order': step.order
                            } for step in process.designprocessstep_set.all()
                        ]
                    } for process in project.design_processes.all()
                ],
                'pages': [
                    {
                        'id': page.id,
                        'title': page.title,
                        'text_layers': [
                            {
                                'id': text_layer.id,
                                'title': text_layer.title,
                                'text': text_layer.text,
                                'order': text_layer.order
                            } for text_layer in page.text_layers.all()
                        ],
                        'image_layers': [
                            {
                                'id': image_layer.id,
                                'title': image_layer.title,
                                'image': image_layer.image.url if image_layer.image else None,
                                'alt_text': image_layer.alt_text,
                                'text': image_layer.text,
                                'order': image_layer.order,
                                'links': [
                                    {
                                        'id': link.id,
                                        'title': link.title,
                                        'url': link.url,
                                        'description': link.description
                                    } for link in image_layer.links.all()
                                ]
                            } for image_layer in page.image_layers.all()
                        ],
                        'video_layers': [
                            {
                                'id': video_layer.id,
                                'video_url': video_layer.video_url,
                                'order': video_layer.order
                            } for video_layer in page.video_layers.all()
                        ]
                    } for page in project.pages.all()
                ]
            }
            data.append(project_data)

        # 确定导出路径
        output_dir = 'path/to/export'  # 设定导出路径

        # 如果目录不存在，则创建目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 导出 JSON 文件
        file_path = os.path.join(output_dir, 'data.json')
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(data)} projects to {file_path}'))
