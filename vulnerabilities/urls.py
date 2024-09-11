from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_vulnerabilities),
    path('fixed/', views.fixed_vulnerabilities),
    path('unfixed/', views.unfixed_vulnerabilities),
    path('get-unfixed/', views.get_unfixed_vulnerabilities),
    path('resumen/', views.get_vulnerabilities_by_severity),
]
