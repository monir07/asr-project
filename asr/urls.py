
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from custom_auth.views import Dashboard, gentella_html
from custom_auth.views import (UserLoginView, SignUpCreateView, UserLogoutView, UserPasswordChangeView)

urlpatterns = [
    path('home/', Dashboard.as_view(), name='dashboard'),
    
    re_path(r'^.*\.html', gentella_html, name='gentella'),
    
    path('admin/', admin.site.urls),
    # tender urls
    path('tender/', include('tender.urls')),
    # custom authentication urls
    path('signup/', SignUpCreateView.as_view(), name='user_signup'),
    path('', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('password-change/', UserPasswordChangeView.as_view(), name='user_password_change'),

    path('auth/', include('custom_auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ADMIN PANEL HEADER AND TITLE TEXT CHANGE.
admin.site.site_header = "ASR Admin Panel"
admin.site.site_title = "ASR Admin Portal"
admin.site.index_title = "Welcome to ASR Portal"
