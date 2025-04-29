"""
URL configuration for pr1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from myapp.views import property_list, property_create, property_update, property_delete  # Импортируем представления

urlpatterns = [
    path('admin/', admin.site.urls),  # URL для админки
    path('', property_list, name='property_list'),  # Главная страница со списком недвижимости
    path('property/new/', property_create, name='property_create'),  # Страница создания новой недвижимости
    path('property/<int:pk>/edit/', property_update, name='property_update'),  # Страница редактирования недвижимости
    path('property/<int:pk>/delete/', property_delete, name='property_delete'),  # Страница удаления недвижимости
]