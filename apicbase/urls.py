from django.contrib import admin
from manager import urls as manager_urls
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('admin/', admin.site.urls),
    path('manager/', include(manager_urls))
]
