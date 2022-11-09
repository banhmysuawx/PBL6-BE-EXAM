from django.urls import path
from .views import TestView, DoTestView
urlpatterns = [
    path('test', TestView.as_view({'get':'list', 'post':'create'})),
    path('test/<int:pk>', TestView.as_view({'get':'retrieve'})),
    path('test/<int:pk>/doing', DoTestView.as_view({'post':'doing_test'})),
]
