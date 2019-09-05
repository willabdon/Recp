from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from manager import urls as manager_urls
from .views import redirect_view, LoginView, LogoutView, SignupView

urlpatterns = [
    path('', redirect_view),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('admin/', admin.site.urls),
    path('manager/', include(manager_urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
