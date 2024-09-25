"""
URL configuration for pythagore project.

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
from django.urls import include, path


from faunatrack import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name="base"),
    path('bonjour/', views.home, name="home"),
    path('projets/', views.ProjetList.as_view(), name="projets_list"),
    path('projets/add/', views.ProjetCreate.as_view(), name="projet_create"),
    path('projets/<str:slug>/', views.ProjetDetail.as_view(), name="projet_detail"),
    path('projets/<str:slug>/edit/', views.ProjetUpdate.as_view(), name="projet_update"),
    path('projets/<str:slug>/delete/', views.ProjetDelete.as_view(), name="projet_delete"),
    path('test/', views.projet_with_2_project_displayed, name="projet_test"),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('faunatrack.urls_api')),
    
]  
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)