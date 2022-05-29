from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('submit/', views.UserQuestionView.as_view()),
    path('similar/<int:pk>/', views.SimilarClothesView.as_view()),
    path('more_questions/', views.MoreQuestionsView.as_view()),
    path('get_pics/', views.NormalView.as_view()),
]
