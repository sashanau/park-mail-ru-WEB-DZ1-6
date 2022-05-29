from django.urls import path, include
from app import views

urlpatterns = [
    path('ask/', views.ask, name="ask"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('hot/', views.hot, name="hot"),
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('question/<int:number>', views.question, name="question"),
    path('register/', views.register, name="register"),
    path('settings/', views.settings, name="settings"),
    path('vote/', views.vote, name="vote"),
    path('logout/', views.logout, name="logout"),
    path('vote-ans/', views.is_correct, name="is_correct"),
]
