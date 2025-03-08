from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('update_user/', views.update_user, name="update_user"),
    path('create_room/', views.create_room, name="create_room"),
    path('update_room/<str:pk>', views.update_room, name="update_room"),
    path('delete_room/<str:pk>', views.delete_room, name="delete_room"),
    path('delete_message/<str:pk>', views.delete_message, name="delete_message"),
    path('topics-page/', views.topics_page, name="topics_page"),
    path('activity-page/', views.activity_page, name="activity_page"),
]
