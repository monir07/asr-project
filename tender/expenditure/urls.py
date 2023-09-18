from django.urls import path
from .views import *

urlpatterns = [
    path('form-create/',ExpenditureCreateView.as_view(),name='expenditure_form_create'),
    path('form-update/<int:pk>',ExpenditureUpdateView.as_view(),name='expenditure_form_update'),
    path('list/',ExpenditureListView.as_view(),name='expenditure_list'),
    path('delete/<int:pk>',ExpenditureDeleteView.as_view(),name='expenditure_delete'),
]
