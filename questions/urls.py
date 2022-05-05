from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('submit/', views.UserQuestionView.as_view()),
]