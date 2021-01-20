"""anforderungenundtesten URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

#das ist nur eine Liste in Python lol --> Darum ist sie erweiterbar mit +=
urlpatterns = [
    path('aut/', include('aut.urls')), #wenn hier nichts steht landet die Seite bei http://127.0.0.1:8000/ --> könnte man als Hauptseite machen
    path('admin/', admin.site.urls),
]
#Add URL maps to redirect the base URL to our application
#immer auf die App umlenken lassen auch wenn http://127.0.0.1:8000 aufgerufen wird

from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/aut/')),

    #Add Django site authentication urls (for login, logout, password management)
    #durch das include von django... hat man schon die richtigen URLs wie oben beim Admin
    path('accounts/', include('django.contrib.auth.urls')),

]
from django.conf.urls import url
from aut import views as core_views

urlpatterns += [
    url('signup/', core_views.signup, name='signup'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)