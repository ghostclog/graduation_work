import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Users/admin/Desktop/coding/project/django/project/the_project')  # Django 프로젝트 경로를 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_project.settings')
application = get_wsgi_application()
