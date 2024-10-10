"""
URL configuration for taskpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/add/',views.TaskCreateView.as_view(),name="task_add"),
    path('task/list/',views.TaskListView.as_view(),name="task_list"),
    path('task/<int:pk>/change',views.TaskUpdateView.as_view(),name="task_update"),
    path('task/<int:pk>/remove',views.TaskDeleteView.as_view(),name="task_delete"),
    path('register/',views.SignUpView.as_view(),name="user"),
    path('signin/',views.SignInView.as_view(),name="signin"),
    path('signout/',views.SignOutView.as_view(),name="logout"),
    path('summary/',views.TaskSummaryView.as_view(),name="summary")
]
