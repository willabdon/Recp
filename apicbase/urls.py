from django.contrib import admin
from django.urls import path, include

from manager import urls as manager_urls
from .views import redirect_view, LoginView, LogoutView

urlpatterns = [
    path('', redirect_view),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('manager/', include(manager_urls))
]
