from django.urls import path, include
from . import views


urlpatterns = [
     path('refbooks/', views.RefbookListView.as_view(), name='refbook-list'),
     path('refbooks/<int:pk>/elements/', views.RefbookElementListView.as_view(),
         name='refbook-element-list'),
     path('refbooks/<int:pk>/check_element/', views.RefbookElementCheckView.as_view(),
         name='refbook-check-element'),
]
