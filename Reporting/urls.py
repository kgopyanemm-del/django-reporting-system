from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.home,            name='home'),
    path('report/',             views.report_issue,    name='report_issue'),
    path('report/success/<str:ref>/', views.report_success, name='report_success'),
    path('reports/',            views.report_list,     name='report_list'),
    path('province/',           views.province_reports, name='province_reports'),
]