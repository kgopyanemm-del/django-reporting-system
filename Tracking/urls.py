from django.urls import path
from . import views

urlpatterns = [
    path('track/',                         views.track_home,      name='track_home'),
    path('track/report/<int:pk>/',         views.report_detail,   name='report_detail'),
    path('track/report/<int:pk>/update/',  views.update_status,   name='update_status'),
    path('track/report/<int:pk>/feedback/',views.submit_feedback,  name='submit_feedback'),
    path('api/pins/',                      views.map_pins_json,   name='map_pins_json'),
]