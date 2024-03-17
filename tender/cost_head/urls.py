from django.urls import path
from .views import GetSubHeadAPIView

urlpatterns = [
    path('sub-head/api/<int:pk>/', GetSubHeadAPIView.as_view(), name="get_sub_head_api"),
]