
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from custom_auth.views import Dashboard

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    
    path('admin/', admin.site.urls),
    # tender urls
    path('tender/', include('tender.urls')),
    # custom authentication urls
    path('auth/', include('custom_auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ADMIN PANEL HEADER AND TITLE TEXT CHANGE.
admin.site.site_header = "ASR Admin"
admin.site.site_title = "ASR Admin Portal"
admin.site.index_title = "Welcome to ASR Portal"
