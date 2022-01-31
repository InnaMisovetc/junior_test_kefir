from django.contrib import admin
from django.urls import path, include
from .drf_spectacular import urlpatterns as doc_urls

urlpatterns = [
    path('', include('user_session.urls')),
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
    path('private/users', include('users_administration.urls'))
]

urlpatterns += doc_urls
