"""lavenue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.urls import include, path

from organisations.views import HomeView
from users import urls as user_urls

from organisations import urls as organization_urls
# from speakers.views import intervention_create_view, motion_create_view, vote_create_view

urlpatterns = [
	path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(user_urls)),
	path('__debug__/', include(debug_toolbar.urls)),
    path('organisations/', include(organization_urls)),
    path('', HomeView.as_view(), name='landing-view'),
    # path('secretary/', intervention_create_view),
    # path('secretary/', motion_create_view),
    # path('secretary/', vote_create_view),
] 
