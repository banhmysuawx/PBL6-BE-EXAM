from django.urls import path
from .views import TestView, DoTestView, CategoryView, ResultView, QuestionView
urlpatterns = [
    path('test', TestView.as_view({'get':'list', 'post':'create'})),
    path('test/<int:pk>', TestView.as_view({'get':'retrieve', 'delete':'destroy'})),
    path('test/<int:pk>/doing', DoTestView.as_view({'post':'doing_test'})),
    path('test/category', CategoryView.as_view()),
    path('test/question', QuestionView.as_view({'get':'list'})),
    path('test/question/<int:pk>', QuestionView.as_view({'get':'retrieve'})),
    path('results', ResultView.as_view({'get':'list'})),
    # path("result/<int:user_id>/", ResultView.as_view({'get':'retrieve', 'delete':'destroy'})),
    path("results/<int:user_id>/jobs/<int:job_id>/", ResultView.as_view({'get':'retrieve', 'delete':'destroy'})),
]
